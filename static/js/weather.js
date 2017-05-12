
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
<script>
jQuery(document).ready(function($) {
  $.ajax({
  url : "http://api.wunderground.com/api/3e18519d13a0ee9d/geolookup/conditions/q/IA/Cedar_Rapids.json",
  dataType : "jsonp",
  success : function(parsed_json) {
  var location = parsed_json['location']['city'];
  var temp_f = parsed_json['current_observation']['temp_f'];
  alert("Current temperature in " + location + " is: " + temp_f);
  }
  });
});
</script>

var v1 = parsed_json['forecast']['txt_forecast']['forecastday'];
                for (index in v1) {
                    alert('Weather forecast for '+v1[index]['title']+' is '+v1[index]['fcttext_metric']);

