$(function() {
  $("article.hunch article.evidence section.vote").each(function() {
    var $vote = $(this);

    $vote.find("div.choice input").click(function() {
      $(this).closest("form").submit();
    });
  });
});