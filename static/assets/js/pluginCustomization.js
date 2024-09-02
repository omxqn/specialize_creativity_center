
"use strict";
$(document).ready(function () {

  // nice select 
  $('select').niceSelect();
  
  // chart js 
  // bar chart 
  var monthlyUserChart = document.getElementById('monthlyUserChart')
  if (monthlyUserChart){

    let yValue = [62, 75, 62, 85, 70, 78, 58, 70, 42, 5, 5, 5]
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    let bgColor = ['#53A2F6', '#28A745', '#FD0049', '#FFC107',]
  
    new Chart(monthlyUserChart, {
      type: 'bar',
      data: {
        labels: months,
        datasets: [{
          data: yValue,
          borderWidth: 1,
          borderRadius: 5,
          backgroundColor: bgColor,
          maxBarThickness: 28,
        }]
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            min: 0,
            max: 100,
            ticks: {
              padding: 20,
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        },
  
        plugins: {
          legend: {
            display: false,
          },
          labels: {
            display: true
          }
        }
      }
    });
  }

  // donut Chart
  // 1st 15 days Analytics
  var FFDa = document.getElementById("ffda");
  if (FFDa) {
    new Chart(FFDa, {
      type: 'doughnut',
      data: {
        datasets: [{
          label: 'first 15 days Analytics',
          data: [80, 40],
          backgroundColor: ['#53A2F6', '#EDEDED'],
          hoverOffset: 2
        }],
      },
  
      options: {
        responsive: true,
        cutout: 35,
        borderRadius: 10,
      },
      plugins: [{
        id: 'text',
        beforeDraw: function (chart, a, b) {
          var width = chart.width,
            height = chart.height,
            ctx = chart.ctx;
  
          ctx.restore();
          var fontSize = (height / 114).toFixed(2);
          ctx.font = fontSize + "em sans-serif";
  
          var text = "-40.56%",
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = height / 2;
  
          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });
  }

  // last 15 days Analytics
  var LFDa = document.getElementById("lfda");
  if(LFDa){
    new Chart(LFDa, {
      type: 'doughnut',
      data: {
        datasets: [{
          label: 'last 15 days Analytics',
          data: [70, 25],
          backgroundColor: ['#FFC107', '#EDEDED'],
          hoverOffset: 2
        }],
      },
      options: {
        responsive: true,
        cutout: 35,
        borderRadius: 10,
      },
  
      plugins: [{
        id: 'text',
        beforeDraw: function (chart, a, b) {
          var width = chart.width,
            height = chart.height,
            ctx = chart.ctx;
  
          ctx.restore();
          var fontSize = (height / 114).toFixed(2);
          ctx.font = fontSize + "em sans-serif";
  
          var text = "-30.56%",
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = height / 2;
  
          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });
  }

  // 1st 15 days Analytics
  var ffd = document.getElementById("ffd");
  if(ffd){
    new Chart(ffd, {
      type: 'doughnut',
      data: {
        datasets: [{
          label: 'first 15 days Analytics',
          data: [80, 40],
          backgroundColor: ['#53A2F6', '#EDEDED'],
          hoverOffset: 2
        }],
      },
  
      options: {
        responsive: true,
        cutout: 35,
        borderRadius: 10,
      },
      plugins: [{
        id: 'text',
        beforeDraw: function (chart, a, b) {
          var width = chart.width,
            height = chart.height,
            ctx = chart.ctx;
  
          ctx.restore();
          var fontSize = (height / 114).toFixed(2);
          ctx.font = fontSize + "em sans-serif";
  
          var text = "-40.56%",
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = height / 2;
  
          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });
  }

  // last 15 days Analytics
  var lfd = document.getElementById("lfd");
  if(lfd){
    new Chart(lfd, {
      type: 'doughnut',
      data: {
        datasets: [{
          label: 'last 15 days Analytics',
          data: [70, 25],
          backgroundColor: ['#FFC107', '#EDEDED'],
          hoverOffset: 2
        }],
      },
      options: {
        responsive: true,
        cutout: 35,
        borderRadius: 10,
      },
  
      plugins: [{
        id: 'text',
        beforeDraw: function (chart, a, b) {
          var width = chart.width,
            height = chart.height,
            ctx = chart.ctx;
  
          ctx.restore();
          var fontSize = (height / 114).toFixed(2);
          ctx.font = fontSize + "em sans-serif";
  
          var text = "-30.56%",
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = height / 2;
  
          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });
  }

    // 30 days Analytics
    var tda = document.getElementById("tda");
    if(tda){
      new Chart(tda, {
        type: 'doughnut',
        data: {
          datasets: [{
            label: '30 days Analytics',
            data: [70, 25],
            backgroundColor: ['#53A2F6', '#EDEDED'],
            hoverOffset: 2
          }],
        },
        options: {
          responsive: true,
          cutout: 22.5,
          borderRadius: 10,
        },
    
        plugins: [{
          id: 'text',
          beforeDraw: function (chart, a, b) {
            var width = chart.width,
              height = chart.height,
              ctx = chart.ctx;
    
            ctx.restore();
            var fontSize = (height / 114).toFixed(2);
            ctx.font = fontSize + "em sans-serif";
    
            var text = "-81.08%",
              textX = Math.round((width - ctx.measureText(text).width) / 2),
              textY = height / 2;
    
            ctx.fillText(text, textX, textY);
            ctx.save();
          }
        }]
      });
    }


});