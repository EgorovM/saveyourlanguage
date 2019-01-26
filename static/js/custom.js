

var canvas = new fabric.Canvas('canvas');
var counter = 0;

canvas.isDrawingMode = true;
canvas.freeDrawingBrush.width = 20;
canvas.freeDrawingBrush.color = "#000000";
canvas.backgroundColor = "#ffffff";
canvas.renderAll();


// Clear button callback
$("#clear-canvas").click(function(){ 
  $(".result").text("");  
  canvas.clear(); 
  canvas.backgroundColor = "#ffffff";
  canvas.renderAll();
  updateChart(zeros);
  $("#status").removeClass();

});

// // Predict button callback
// $("#predict").click(function(){  
//   counter++;

//   if(counter == 1) $(".result").text("Это буква о");
//   if(counter == 2) $(".result").text("Это буква ө");
//   if(counter == 3) $(".result").text("Это буква ү");
//   if(counter == 4) $(".result").text("Это буква г");
//   if(counter == 5) $(".result").text("Это буква ҕ");
//   if(counter == 6) $(".result").text("Это буква h");
//   if(counter == 7) $(".result").text("Это буква ҥ");
//   if(counter == 8) $(".result").text("Это буква а");
//   if(counter == 9) $(".result").text("Это буква б");
//   if(counter == 10) $(".result").text("Это буква х");
//   if(counter == 11) $(".result").text("Это буква 1");
//   if(counter == 12) $(".result").text("Это буква 5");
//   if(counter == 13) $(".result").text("Это буква 7");
// });

