<div class="container">
  <div class="row mb-4">
    <div class="col-12 text-center">
      <div class="mb-3">
        <!-- Logo Placeholder -->
        <img src="https://www.wvm.edu/_resources/images/wvm-logo.svg" alt="West Valley - Mission CCD" class="img-fluid" style="max-height: 80px;">
      </div>
      <h1>Record Your Name with Name Coach</h1>
      <p class="lead">Help your instructors and peers pronounce your name correctly</p>
    </div>
  </div>
  
  <div class="row mb-5">
    <div class="col-lg-6">
      <div class="card">
        <div class="card-body text-center py-5">
          <h3 class="mb-4">Ready to Record Your Name?</h3>
          <p class="mb-4">Click the button below to open the recording interface and capture your name pronunciation.</p>
          <button data-toggle="nc-widget"
                  class="btn-record"
                  data-attributes-email-presentation="readonly"
                  data-attributes-first-name-presentation="readonly"
                  data-attributes-middle-name-value=""
                  data-attributes-last-name-presentation="readonly"
                  data-attributes-notes-presentation="hidden">
            Record My Name
          </button>
        </div>
      </div>
    </div>
    <div class="col-lg-6 mb-4">
      <h2>How It Works</h2>
      <div class="how-it-works-step">
        <div class="step-number">1</div>
        <h4>Click the "Record My Name" button</h4>
        <p>When you click the button, the Name Coach recording widget will open directly in your browser.</p>
      </div>
      <div class="how-it-works-step">
        <div class="step-number">2</div>
        <h4>Record your name</h4>
        <p>Use your device's microphone to record the correct pronunciation of your name. You can listen to and re-record until you're satisfied.</p>
      </div>
      <div class="how-it-works-step">
        <div class="step-number">3</div>
        <h4>Save and confirm</h4>
        <p>Click "Save changes" to store your recording. Your name pronunciation will be available to your instructors through the college learning management system.</p>
      </div>
    </div>
  </div>
  
  <div class="row">
    <div class="col-md-12">
      <!-- FAQ section commented out
      <div class="card">
        <div class="card-body">
          <h3>Frequently Asked Questions</h3>
          
          <div class="mt-4">
            <h5>Do I need special equipment to record my name?</h5>
            <p>No, you only need a device with a microphone (built into most computers, laptops, and mobile devices).</p>
          </div>
          
          <div class="mt-3">
            <h5>Who will have access to my recording?</h5>
            <p>Your instructors and authorized college staff will have access to hear your name pronunciation.</p>
          </div>
          
          <div class="mt-3">
            <h5>Can I re-record my name?</h5>
            <p>Yes, you can return to this page anytime to record a new pronunciation.</p>
          </div>
          
          <div class="mt-3">
            <h5>Is this required?</h5>
            <p>While recording your name is optional, we strongly encourage you to use this service to help your instructors and peers pronounce your name correctly.</p>
          </div>
        </div>
      </div>
      -->
    </div>
  </div>
</div>

<script type="text/javascript" src="https://nc-widget-v3.s3.us-east-2.amazonaws.com/bundle.js"> </script>
<script>
    ncE(function() {
        ncE.configure(function(config) {
            config.eventCode = "C11E08";
            config.accessToken = "47963erHHLSzTJdczDj7";
            config.brandColor = "#0d4268";
            config.embedded = false;
            config.dictionary = {
               web_recorder_button_label: "Record My Name",
               pitch_max_value_label: "High",
               pitch_min_value_label: "Low",
               pitch_set_default_link_label: "Default",
               pitch_slider_label: "Adjust recording audio pitch",
               only_web_recorder: false,
               web_recorder_auto_submit: true,
               call_session_auto_submit: true
            };
            config.customStyles = {
               playBackBtnColor: "000000",
               recordBtnColor: "#0d4268",
               showBox: "false",
               pitchTrackColor: "#0d4268",
               pitchThumbColor: "00000"
            };
            config.kioskOptions = {
              pitchEnabled: true,
              webRecorderOnly: true,
              enableAutoSubmit: true
            };
         });
    });
</script>