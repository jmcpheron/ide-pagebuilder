<script>

function drawTermDropdown(selected_term){
    
      url = '/BannerExtensibility/internalPb/virtualDomains.efg_terms';
        $.ajax({
        url: url,
        method: "GET",
        data: { 
          max: 300,
          offset: "0"
          }
      })
      .done(function(data) {
          $("#term-dropdown").html("<label for='term'>Select or change term</label><select id='term' name='term'  class='form-select'></select>");
    
    var output = [];
    
    $.each(data, function(key, v)
    { 
      selected = "";
      if(v["EFG_TERM"] == selected_term){
        selected = " SELECTED ";
      }
      output.push('<option value="'+ v["EFG_TERM"] +'" '+selected + '>'+ v["STVTERM_DESC"] +'</option>');
    });
    
    $('#term').html(output.join(''));
    
       //$("#term-dropdown").append("</select>");
       $("#term-dropdown").change(function(){
            new_term = $( "#term-dropdown option:selected" ).val();
            window.open("?term=" + new_term,"_self")
        });
    
      });
    
};

function getFtInfo(term){
var url= '/BannerExtensibility/internalPb/virtualDomains.free_tuition_single';
$.ajax({
    headers: { 
	'Accept': 'application/json',
	'Content-Type': 'application/json' 
    },
    'type': 'GET',
    'url': url,
    'dataType': 'json',
        data: { 
          max: 1,
          offset: "0",
          'term': term
          }

    })
    .done(function(data){
      console.log( data[0]);
      var how_good = 0;

      if(data[0]['EMPLOYEE_IND'] == 'Y'){
        $("#emp-inelg").show();
        how_good--; 
        console.log(how_good);
      }

      if(data[0]['FAFSA_IND'] == 'Y'){
        $("#no-1").hide();
        $("#req-1").hide();
        $("#yes-1").show();
        how_good++;
      }

      if(data[0]['LEVEL_CODE'] == 'CR'){
        $("#no-2").hide();
        $("#req-2").hide();
        $("#yes-2").show();
        how_good++;      }

      if(data[0]['DECODE_RESD_CODE'] == 'Y'){
        $("#no-3").hide();
        $("#req-3").hide();
        $("#yes-3").show();
        how_good++;      }

//      if(data[0]['SERVICE_ZIP_IND'] == 'Y'){
      if( (data[0]['SERVICE_ZIP_IND'] == 'Y') || (data[0]['EXEMPT_LVL'] == 'AA') ){
        $("#no-4").hide();
        $("#req-4").hide();
        $("#yes-4").show();
        how_good++;
      }
  if(how_good >= 4){
    $("#wvm-success").show();
    $("#wvm-no").hide();
  }else{
    $("#wvm-no").show();
    console.log('Not met');
}
  $("#wvm-loading-gif").hide();
  $("#ft-results").show();

      if(data[0]['EMPLOYEE_IND'] == 'Y'){
        $("#emp-inelg").show();
        $("#ft-results").hide();
        $("#wvm-no").hide();
      }

  })
   .fail(function( jqXHR, textStatus ) {
     console.log( "Request failed: " + textStatus );
    })//end fail
}

</script>