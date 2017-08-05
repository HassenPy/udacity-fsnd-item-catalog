$(function(){
  $("time.timeago").timeago();
  var authors = $(".author");
  authors.each(function(author){
    elm = $(authors[author]);
    url = elm.data('author');
    $.ajax({
        method: "GET",
        url: url,
        context: elm,
        success: function(response){
          var username = response['username'];
          this.html('by ' + username);
        }
      });
    });

    $('#deleteModal').on('shown.bs.modal', function (e) {
      e.preventDefault();
    });
    $('.delete').click(function(e){
      $('#deleteButton').data('action', $(this).data('href'));
      e.preventDefault();
    });
    $('#deleteButton').click(function(e){
      $.ajax({
        method: "DELETE",
        url: $(this).data('action')
      });
    });

});
