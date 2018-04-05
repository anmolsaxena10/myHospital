$(document).ready(function(){
  $(".button-collapse").sideNav();
  $('select').material_select();
  $('.collapsible').collapsible();

  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //January is 0!
  var yyyy = today.getFullYear();
   if(dd<10){
          dd='0'+dd
      }
      if(mm<10){
          mm='0'+mm
      }

  today = yyyy+'-'+mm+'-'+dd;
  if(document.getElementById("appointment_date")){
    document.getElementById("appointment_date").setAttribute("min", today);
  }
  if(document.getElementById("dob")){
    document.getElementById("dob").setAttribute("max", today);
  }
  var patient_data, doctor_data, case_data;
  if(document.getElementById('patient-data')){
    temp = '{' + $("#patient-data").html().slice(0, $("#patient-data").html().length-2) + '}';
    patient_data = JSON.parse(temp);
    console.log(patient_data);
  }
  if(document.getElementById('doctor-data')){
    temp = '{' + $("#doctor-data").html().slice(0, $("#doctor-data").html().length-2) + '}';
    doctor_data = JSON.parse(temp);
    console.log(doctor_data);
  }
  //if(document.getElementById('case-data')){
    //temp = '{' + $("#case-data").html().slice(0, $("#case-data").html().length-2) + '}';
    //case_data = JSON.parse(temp);
    //console.log(case_data);
  //}

  $('input.autocomplete-patient').autocomplete({
    data: patient_data,
    limit: 20,
    onAutocomplete: function(val) {

    },
    minLength: 1,
  });

  $('input.autocomplete-doctor').autocomplete({
    data: doctor_data,
    limit: 20,
    onAutocomplete: function(val) {

    },
    minLength: 1,
  });

  //$('input.autocomplete-case').autocomplete({
    //data: case_data,
    //limit: 20,
    //onAutocomplete: function(val) {

    //},
    //minLength: 1,
  //});
});
