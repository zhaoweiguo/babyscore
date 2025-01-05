// 添加AJAX请求以获取数据
fetch('/get_action_logs/')
    .then(response => response.json())
    .then(data => {
        const actionLogs = data;
        const pointsData = actionLogs.map(log => log.points_change);
        const timeLabels = actionLogs.map(log => new Date(log.timestamp));

        // 计算累计积分
        const cumulativePoints = pointsData.reduce((acc, curr) => {
            acc.push(acc[acc.length - 1] + curr);
            return acc;
        }, [0]);

        // 添加时间分组函数
        function groupByTimeUnit(labels, points, unit) {
            const groupedData = {};
            labels.forEach((label, index) => {
                const date = new Date(label);
                let key;
                switch (unit) {
                    case 'day':
                        key = date.toISOString().split('T')[0];
                        break;
                    case 'hour':
                        key = date.toISOString().slice(0, 13);
                        break;
                    case 'week':
                        const weekStart = new Date(date.setDate(date.getDate() - date.getDay()));
                        key = weekStart.toISOString().split('T')[0];
                        break;
                    case 'month':
                        key = date.toISOString().slice(0, 7);
                        break;
                    default:
                        key = date.toISOString().split('T')[0];
                }
                if (!groupedData[key]) {
                    groupedData[key] = { points: 0, count: 0 };
                }
                groupedData[key].points += points[index];
                groupedData[key].count += 1;
            });
            return Object.keys(groupedData).map(key => ({
                label: key,
                points: groupedData[key].points
            })).sort((a, b) => new Date(a.label) - new Date(b.label));
        }

        // 初始化数据
        let groupedData = groupByTimeUnit(timeLabels, cumulativePoints, 'day');
        let chartLabels = groupedData.map(item => item.label);
        let chartData = groupedData.map(item => item.points);

        // 创建折线图
        const ctx = document.getElementById('pointsChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartLabels,  // 使用时间标签作为X轴
                datasets: [{
                    label: '累计积分',
                    data: chartData,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',  // 默认时间单位为天
                            tooltipFormat: 'yyyy-MM-dd HH:mm:ss'  // 添加时间提示格式
                        },
                        title: {
                            display: true,
                            text: '时间'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: '累计积分'
                        }
                    }
                }
            }
        });

        // 添加事件监听器以处理时间单位选择变化
        document.getElementById('timeUnit').addEventListener('change', function(event) {
            const selectedUnit = event.target.value;

            // 更新分组数据
            groupedData = groupByTimeUnit(timeLabels, cumulativePoints, selectedUnit);
            chartLabels = groupedData.map(item => item.label);
            chartData = groupedData.map(item => item.points);

            // 更新图表数据
            chart.data.labels = chartLabels;
            chart.data.datasets[0].data = chartData;
            chart.options.scales.x.time.unit = selectedUnit;
            chart.update();
        });
    })
    .catch(error => console.error('Error fetching action logs:', error));