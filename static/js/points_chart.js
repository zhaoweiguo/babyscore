// 添加AJAX请求以获取数据
fetch('/get_action_logs/')
    .then(response => response.json())
    .then(data => {
        const actionLogs = data;
        const pointsData = actionLogs.map(log => log.points_change);
        const rewardData = actionLogs.filter(log => log.points_change > 0).map(log => log.points_change);
        const punishmentData = actionLogs.filter(log => log.points_change < 0).map(log => log.points_change);
        const timeLabels = actionLogs.map(log => new Date(log.timestamp));

        // 计算累计积分
        const cumulativePoints = pointsData.reduce((acc, curr) => {
            acc.push(acc[acc.length - 1] + curr);
            return acc;
        }, [0]);

        // 计算累计奖励积分
        const cumulativeRewards = rewardData.reduce((acc, curr) => {
            acc.push(acc[acc.length - 1] + curr);
            return acc;
        }, [0]);

        // 计算累计惩罚积分
        const cumulativePunishments = punishmentData.reduce((acc, curr) => {
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
        let totalGroupedData = groupByTimeUnit(timeLabels, cumulativePoints, 'day');
        let rewardGroupedData = groupByTimeUnit(timeLabels, cumulativeRewards, 'day');
        let punishmentGroupedData = groupByTimeUnit(timeLabels, cumulativePunishments, 'day');

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
                            text: '累计惩罚积分'
                        }
                    }
                }
            }
        });

        // 添加事件监听器以处理时间单位选择变化
        document.getElementById('timeUnit').addEventListener('change', function(event) {
            const selectedUnit = event.target.value;

            // 更新分组数据
            totalGroupedData = groupByTimeUnit(timeLabels, cumulativePoints, selectedUnit);
            rewardGroupedData = groupByTimeUnit(timeLabels, cumulativeRewards, selectedUnit);
            punishmentGroupedData = groupByTimeUnit(timeLabels, cumulativePunishments, selectedUnit);

            totalChartLabels = totalGroupedData.map(item => item.label);
            totalChartData = totalGroupedData.map(item => item.points);
            rewardChartLabels = rewardGroupedData.map(item => item.label);
            rewardChartData = rewardGroupedData.map(item => item.points);
            punishmentChartLabels = punishmentGroupedData.map(item => item.label);
            punishmentChartData = punishmentGroupedData.map(item => item.points);

            // 更新图表数据
            totalChart.data.labels = totalChartLabels;
            totalChart.data.datasets[0].data = totalChartData;
            totalChart.options.scales.x.time.unit = selectedUnit;
            totalChart.update();

            rewardChart.data.labels = rewardChartLabels;
            rewardChart.data.datasets[0].data = rewardChartData;
            rewardChart.options.scales.x.time.unit = selectedUnit;
            rewardChart.update();

            punishmentChart.data.labels = punishmentChartLabels;
            punishmentChart.data.datasets[0].data = punishmentChartData;
            punishmentChart.options.scales.x.time.unit = selectedUnit;
            punishmentChart.update();
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