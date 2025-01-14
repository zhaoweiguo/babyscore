// 添加AJAX请求以获取数据
fetch('/api/points_data')
    .then(response => response.json())
    .then(data => {
        const totalGroupedData = data.total;
        const rewardGroupedData = data.rewards;
        const punishmentGroupedData = data.punishments;

        let totalChartLabels = totalGroupedData.map(item => item.label);
        let totalChartData = totalGroupedData.map(item => item.points);
        let rewardChartLabels = rewardGroupedData.map(item => item.label);
        let rewardChartData = rewardGroupedData.map(item => item.points);
        let punishmentChartLabels = punishmentGroupedData.map(item => item.label);
        let punishmentChartData = punishmentGroupedData.map(item => item.points);

        // 创建总积分变化折线图
        const totalCtx = document.getElementById('totalChart').getContext('2d');
        const totalChart = new Chart(totalCtx, {
            type: 'line',
            data: {
                labels: totalChartLabels,  // 使用时间标签作为X轴
                datasets: [{
                    label: '累计积分',
                    data: totalChartData,
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
                            tooltipFormat: 'yyyy年MM月dd日'  // 添加时间提示格式
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

        // 创建奖励积分变化折线图
        const rewardCtx = document.getElementById('rewardChart').getContext('2d');
        const rewardChart = new Chart(rewardCtx, {
            type: 'line',
            data: {
                labels: rewardChartLabels,  // 使用时间标签作为X轴
                datasets: [{
                    label: '累计奖励积分',
                    data: rewardChartData,
                    borderColor: 'rgba(76, 175, 80, 1)',
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
                            tooltipFormat: 'yyyy年MM月dd日'  // 添加时间提示格式
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
                            text: '累计奖励积分'
                        }
                    }
                }
            }
        });

        // 创建惩罚积分变化折线图
        const punishmentCtx = document.getElementById('punishmentChart').getContext('2d');
        const punishmentChart = new Chart(punishmentCtx, {
            type: 'line',
            data: {
                labels: punishmentChartLabels,  // 使用时间标签作为X轴
                datasets: [{
                    label: '累计惩罚积分',
                    data: punishmentChartData,
                    borderColor: 'rgba(255, 0, 0, 1)',
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
                            tooltipFormat: 'yyyy年MM月dd日'  // 添加时间提示格式
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
                            text: '累计惩罚积分'
                        }
                    }
                }
            }
        });

        // 添加事件监听器以处理时间单位选择变化
        document.getElementById('timeUnit').addEventListener('change', function(event) {
            const selectedUnit = event.target.value;

            // 发送请求以获取新的分组数据
            fetch(`/api/points_data?time_unit=${selectedUnit}`)
                .then(response => response.json())
                .then(data => {
                    const totalGroupedData = data.total;
                    const rewardGroupedData = data.rewards;
                    const punishmentGroupedData = data.punishments;
                    // console.log(data)

                    let totalChartLabels = totalGroupedData.map(item => item.label);
                    let totalChartData = totalGroupedData.map(item => item.points);
                    let rewardChartLabels = rewardGroupedData.map(item => item.label);
                    let rewardChartData = rewardGroupedData.map(item => item.points);
                    let punishmentChartLabels = punishmentGroupedData.map(item => item.label);
                    let punishmentChartData = punishmentGroupedData.map(item => item.points);

                    // 格式化标签
                    // formatLabels({ labels: totalChartLabels }, selectedUnit);
                    // formatLabels({ labels: rewardChartLabels }, selectedUnit);
                    // formatLabels({ labels: punishmentChartLabels }, selectedUnit);

                    // 更新图表数据
                    totalChart.data.labels = totalChartLabels;
                    totalChart.data.datasets[0].data = totalChartData;
                    totalChart.options.scales.x.time.unit = selectedUnit;

                    if (selectedUnit === 'month') {
                        totalChart.options.scales.x.time.tooltipFormat = 'yyyy年MM月';
                    } else if (selectedUnit === 'week') {
                        totalChart.options.scales.x.time.tooltipFormat = 'yyyy年ww周'; // 显示周
                    } else {
                        totalChart.options.scales.x.time.tooltipFormat = 'yyyy年MM月dd日';
                    }
                    totalChart.update();

                    rewardChart.data.labels = rewardChartLabels;
                    rewardChart.data.datasets[0].data = rewardChartData;
                    rewardChart.options.scales.x.time.unit = selectedUnit;
                    if (selectedUnit === 'month') {
                        rewardChart.options.scales.x.time.tooltipFormat = 'yyyy年MM月';
                    } else if (selectedUnit === 'week') {
                        rewardChart.options.scales.x.time.tooltipFormat = 'yyyy年ww周'; // 显示周
                    } else {
                        rewardChart.options.scales.x.time.tooltipFormat = 'yyyy年MM月dd日';
                    }
                    rewardChart.update();

                    punishmentChart.data.labels = punishmentChartLabels;
                    punishmentChart.data.datasets[0].data = punishmentChartData;
                    punishmentChart.options.scales.x.time.unit = selectedUnit;
                    if (selectedUnit === 'month') {
                        punishmentChart.options.scales.x.time.tooltipFormat = 'yyyy年MM月';
                    } else if (selectedUnit === 'week') {
                        punishmentChart.options.scales.x.time.tooltipFormat = 'yyyy年ww周'; // 显示周
                    } else {
                        punishmentChart.options.scales.x.time.tooltipFormat = 'yyyy年MM月dd日';
                    }
                    punishmentChart.update();
                })
                .catch(error => console.error('Error fetching action logs:', error));
        });

        // 添加事件监听器以处理标签页切换
        document.querySelectorAll('.nav-link').forEach(tab => {
            tab.addEventListener('click', function(event) {
                event.preventDefault();
                const target = event.target.getAttribute('data-bs-target');
                document.querySelectorAll('.tab-pane').forEach(panel => {
                    panel.classList.remove('show', 'active');
                });
                document.querySelector(target).classList.add('show', 'active');
            });
        });
    })
    .catch(error => console.error('Error fetching action logs:', error));

// function formatLabels(data, timeUnit) {
//     if (timeUnit === 'week') {
//         data.labels = data.labels.map(label => {
//             const [year, week] = label.split('-W');
//             return `${year} 第${week.padStart(2, '0')}周`;
//         });
//     }
// }


