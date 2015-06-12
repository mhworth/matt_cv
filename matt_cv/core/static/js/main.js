

var MattCV = {};

/**
 CV View
*/
MattCV.CVView = function () {
	"use strict";
	var self = $(this),
	skillLegend = $(".skill.legend");

	// Public functions
	var registerLegendHighlights = function () {
		$(function () {
			//Bind mouseleave and mouseenter
			skillLegend.on("mouseenter", function (e) {
				// Highlight all of the skills which match this legend's contents
				var selector = $(this).attr("data-selector");
				$(selector).not(".project").addClass("highlighted");
			});

			skillLegend.on("mouseleave", function (e) {
				// Remove the highlighting
				var selector = $(this).attr("data-selector");
				$(selector).removeClass("highlighted");
			});
		});
	}
	this.registerLegendHighlights = registerLegendHighlights;

}

/**
 Skills view
*/
MattCV.SkillsView = function () {
	"use strict";
	var self = $(this),
		currentlySelectedSkill = null,
		skillsList = $("#skills"),
		skills = $(".skill",skillsList);

	//Initialize
	$(function () {

		// Check to see if someone asked to focus on a skill already by passing ?skill=slug
	    var skill = $.query["skill"];
	    
	    $(window).on("click",".showskills",function () {
	    	showSkills();
	    })

	    // Link will send users without JS to another page... prevent this behavior if they have JS
	    $(window).on("click","span.skill, a.skill",function (e){
	    	e.preventDefault();
	        var selectedSkill = $(this).attr("data-skill");
	        if(selectedSkill==currentlySelectedSkill) {
	            return;
	        }
	        currentlySelectedSkill = selectedSkill;
	        showSkill(currentlySelectedSkill,this);
	    })

	    // Trigger the click event on any skills that were selected via query string
	    $("[data-skill='"+skill+"']").trigger('click');
	});


	/**
		Public Functions
	*/

	var showSkill = function (slug,clicked) {
		// Hide all the skills that we don't want to see first
		var skillSelector = "[data-skill='"+slug+"']";
		$("h2, .skill",skillsList).not(skillSelector + ","+skillSelector+" a").fadeTo(600,0.001);

		// Hide all excess skills
		var remainingSkills = $("[data-skill='"+slug+"'].skill",skillsList);
		var remainingSkill = null;
		if(clicked) {
			remainingSkills.not(clicked).fadeTo(600,0.001);
			remainingSkill = $(clicked);
		} else {
			remainingSkills.slice(1).fadeTo(600,0.001);
			remainingSkill = $(remainingSkills[0]);
		}

		// Move the remaining skill to the upper center of the skills div
		var currentPosition = remainingSkill.position();
		var skillWidth = remainingSkill.width();
		var containerWidth = skillsList.width();
		remainingSkill.addClass("focused")
			.css("top",currentPosition.top+"px")
			.css("left",currentPosition.left+"px")
			.animate({ 
        		top: "-="+currentPosition.top+ "px",
        		left: "+="+(containerWidth*0.5 - currentPosition.left - (skillWidth-20)*0.5) + "px",
        		"font-size":"x-large"
      		}, 600 );
      	$(".showskills").show();
      	$("#skill-detail").fadeIn();

      	$.ajax({
      		url:'/service/skills/'+slug+"?format=skill-detail",
      		dataType:'json'
      	})
      	.success(function (data) {
      		
      		var view = data;
      		var detail = $("#skill-detail div.detail");
      		detail.empty();
      		detail.html(Mustache.to_html($("#skill-detail-template").html(),view));
      		$(".showskills").show();
      	})
	}
	this.showSkill = showSkill;

	// Show the skill list, hiding the focus view
	var showSkills = function () {
		// Show all the skills again
		$("h2, .skill",skillsList).removeClass("focused").attr("style","");	
		$(".showskills").hide();
		$("#skill-detail").hide();
		currentlySelectedSkill = null;
	}
	this.showSkills = showSkills;

}







