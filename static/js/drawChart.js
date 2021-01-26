var chart;

function drawChart(data){
  var ctx=document.getElementById("myChart").getContext('2d');

  if (chart) {
      chart.destroy();
  }

  chart = new Chart(ctx, {
      type: 'line',
      data: {

          labels: data[0],
          datasets: [{
              label: '心拍数',
              data: data[1],
              yAxisID: "y-axis-1",
              fill: false,
              backgroundColor: 'rgb(255, 99, 132)',
              borderColor: 'rgb(255, 99, 132)',
          }, ]
      },
      options: {
          scales: {
              yAxes: [
                  {
                      // センサ軸（左）
                      id: "y-axis-1",
                      type: "linear",
                      position: "left",
                      ticks: {
                          max: 150,
                          min: 50,
                          stepSize: 10
                      },
                  }],
              xAxes: [{
                  type: 'time',
                  time: {
                      displayFormats: {
                        hour:'D日H時 '
                      }
                  }
              }]
          },
          tooltips: {
              callbacks: {
                  title: function (tooltipItem, data) {
                      return moment(tooltipItem[0].xLabel).format('YYYY-MM-DD HH:mm')
                  }
              }
          }
      }
  })
  }

  // データ読込
  function reload() {

      // 指定時間を取得
      var times = $('input[name=times]:checked').val();
      // 1,12,24時間の設定
      var param = moment().subtract(times,'hours').format('YYYY-MM-DD HH:mm:ss')

      $.getJSON('/api/logs?created_at__gte=' + param)
          .done(function (source) {
              let data = new Array(2);
              data[0] = _.pluck(source, 'measured_at');
              data[1] = _.pluck(source, 'bpm');
              drawChart(data);
          })
  };

  $(document).ready(function () {
      // ラジオボタンのイベントリスナー
      $('input[name="times"]:radio').on('change', function () {
          reload();
      });
      // 初期化
      reload();
  });
