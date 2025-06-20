<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://name-coach.com/namecoach-call-widget-v1.js"></script>
<style>
   #namecoach-call-widget-phone_number{
    display: "none";
  }
        .name-coach-section {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 30px;
            margin: 40px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        .feature-box {
            background: white;
            border-radius: 8px;
            padding: 20px;
            height: 100%;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
        }
        
        .feature-box:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            color: #0d6efd;
        }
        
        .btn-record {
            background-color: #0d6efd;
            color: white;
            padding: 12px 30px;
            font-size: 1.1rem;
            border-radius: 30px;
            border: none;
            transition: all 0.3s ease;
        }
        
        .btn-record:hover {
            background-color: #0b5ed7;
            transform: scale(1.05);
        }
        
        .how-it-works-step {
            position: relative;
            padding-left: 50px;
            margin-bottom: 20px;
        }
        
        .step-number {
            position: absolute;
            left: 0;
            top: 0;
            width: 36px;
            height: 36px;
            background-color: #0d6efd;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
/* Add these styles to your existing CSS */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  z-index: 1050;
  animation: fadeIn 0.3s;
}

.modal-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 500px;
  width: 90%;
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  z-index: 1051;
  animation: slideIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translate(-50%, -60%); opacity: 0; }
  to { transform: translate(-50%, -50%); opacity: 1; }
}
</style>