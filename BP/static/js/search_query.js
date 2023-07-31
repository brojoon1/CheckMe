$(document).ready(function() {
    $('#bookName').on('input', function() {
      var query = $(this).val();
      if (query.length >= 2) {
        $.ajax({
          url: '/search/',  // 책 검색을 처리하는 URL로 변경해야 합니다.
          data: {
            'query': query
          },
          dataType: 'json',
          success: function(data) {
            var results = $('#bookResults');
            results.empty();
            $.each(data, function(index, item) {
              results.append('<p>' + item.title + '</p>');
            });
          }
        });
      }
    });
  });