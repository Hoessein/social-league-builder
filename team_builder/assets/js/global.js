$( document ).ready(function() {

  $('textarea').autogrow({onInitialize: true});




 //Cloner for infinite input lists
$(".circle--clone--list").on("click", ".circle--clone--add", function () {
    var parent = $(this).parent("li");
    var copy = parent.clone();
    parent.after(copy);
    copy.find("input[type='text'], textarea, select").val("");
    copy.find("*:first-child").focus();
    updatePositions();

  });

  $(".circle--clone--list").on("click", "li:not(:only-child) .circle--clone--remove", function () {
    var parent = $(this).parent("li");
    parent.remove();
    updatePositions();
  });

  function updatePositions() {
    var listPositions = $("ul.circle--clone--list li");
    listPositions.each(function (i) {

      var position_TOTAL_FORMS = $(this).find('#id_position-TOTAL_FORMS');
      position_TOTAL_FORMS.val(listPositions.length);

      var title = $(this).find("input[id*='-title']");
      title.attr("name", "position-" + i + "-title");
      title.attr("id", "id_position-" + i + "-title");

      var information = $(this).find("input[id*='-information']");
      information.attr("name", "position-" + i + "-information");
      information.attr("id", "id_position-" + i + "-information");

      var information = $(this).find("input[id*='-information']");
      information.attr("name", "position-" + i + "-information");
      information.attr("id", "id_position-" + i + "-information");

    });
  }

  // Adds class to selected item
  $(".circle--pill--list a").click(function() {
    $(".circle--pill--list a").removeClass("selected");
    $(this).addClass("selected");
  });

  // Adds class to parent div of select menu
  $(".circle--select select").focus(function(){
   $(this).parent().addClass("focus");
   }).blur(function(){
     $(this).parent().removeClass("focus");
   });

  // Clickable table row
  $(".clickable-row").click(function() {
      var link = $(this).data("href");
      var target = $(this).data("target");

      if ($(this).attr("data-target")) {
        window.open(link, target);
      }
      else {
        window.open(link, "_self");
      }
  });

  // Custom File Inputs
  var input = $(".circle--input--file");
  var text = input.data("text");
  var state = input.data("state");
  input.wrap(function() {
    return "<a class='button " + state + "'>" + text + "</div>";
  });




});