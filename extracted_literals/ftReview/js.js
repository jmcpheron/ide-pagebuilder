<script>
$(document).ready(function(){

var info_box_text = "<b>(04/18/2024): Enrollment Fee Grant | Fall Information ..<br /></b>Current 24-25 Free Application for Federal Student AID (FAFSA) and California Dream Act Application (CADAA) will not display until May 2024. <b>Students waiting for their <i>Fall 2024</i> Enrollment Fee Grant status, please check back for updates.</b>";


info_box_text = "<strong>(11/2024): AB 3158 | Winter / Spring 2025 Information</strong><br />The free tuition waiver will not appear on your financial aid award letter until you enroll in course(s).";




  $("#blue-info-box").html(info_box_text);
  var url_string = window.location.href;
  var url = new URL(url_string);
  
  var selectedTerm = '202450';
  if(url.searchParams.get("term")){
    var selectedTerm = url.searchParams.get("term");
  }

console.log('selectedTerm');
if(selectedTerm.substring(4, 6) <= "50"){
//  console.log( (parseInt(selectedTerm.substring(0, 4)) -1).toString() + '-' + selectedTerm.substring(2, 4));
  $(".fa-year").text( (parseInt(selectedTerm.substring(0, 4)) -1).toString() + '-' + selectedTerm.substring(2, 4));
}else{
//  console.log( selectedTerm.substring(0, 4).toString() + '-' + (parseInt(selectedTerm.substring(2, 4)) + 1).toString() );
  $(".fa-year").text( selectedTerm.substring(0, 4).toString() + '-' + (parseInt(selectedTerm.substring(2, 4)) + 1).toString()  );
}

  $("#wvm-stu-name").html($("#username").html());
  getFtInfo(selectedTerm );

drawTermDropdown(selectedTerm );

$("#emp-deets").click( function(){
  $("#ft-results").toggle();
});

$(".badge").click( function(){
  $("#req-" + $(this).attr("id").slice(-1)).toggle();
});

$(".btn-outline-primary").click( function(){
  console.log( $(this).attr('id') );
  var h_level =  $(this).attr('id').slice(-1);
  $(".badge").each( function(){
    $(this).html("<h" + h_level + ">" + $(this).text() + "</h" + h_level + ">");
  });
  });

});



</script>