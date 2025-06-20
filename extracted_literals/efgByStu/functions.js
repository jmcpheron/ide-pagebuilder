<script>

function drawTermDropdown(selected_term, gid){
    
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
            window.open("?gid=" + gid + "&term=" + new_term,"_self")
        });
    
      });
    
};

function getFtInfo(term, gid){
var url= '/BannerExtensibility/internalPb/virtualDomains.free_tuition_gid';
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
          'term': term,
          'gid': gid
          }

    })
    .done(function(data){
      console.log( data[0]);
      var how_good = 0;
      $("#wvm-stu-name").html(data[0]['STU_NAME'] + '.');

    var addy = "<b>Current Active Address:</b><br />";
    addy+= data[0]['ADDRESS_TYPE'];
    addy+= "<br />";
    addy+= data[0]['STREET1'];
    addy+= "<br />";
    addy+= data[0]['CITY'];
    addy+= ", ";
    addy+= data[0]['STATE'];
    addy+= " ";
    addy+= data[0]['ZIP'];
    addy+= "<br />";
    $("#efg-addy-details").html(addy);

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

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
};

</script>