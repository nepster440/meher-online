let chartInstance = null;

function renderChart(labels, data) {

    const ctx = document.getElementById('chart');

    if (!ctx) return;

    // Detect Dark Mode
    let isDark = document.body.classList.contains('dark-mode');

    let textColor = "#ffffff"; // always white (your requirement)
    let gridColor = isDark ? "rgba(255,255,255,0.1)" : "rgba(255,255,255,0.2)";

    // Neon colors based on theme
    let primaryColor = getComputedStyle(document.body).getPropertyValue('--primary').trim();

    // Destroy previous chart
    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'line', // 🔥 upgraded from bar to line (neon look)
        data: {
            labels: labels,
            datasets: [{
                label: 'Income',
                data: data,
                borderColor: primaryColor,
                backgroundColor: primaryColor + "33", // transparency
                tension: 0.4,
                fill: true,

                // Neon glow effect
                pointRadius: 5,
                pointBackgroundColor: primaryColor,
                pointBorderColor: "#fff",
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1200,
                easing: 'easeInOutQuad'
            },
            plugins: {
                legend: {
                    labels: {
                        color: textColor,
                        font: {
                            size: 14
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: textColor
                    },
                    grid: {
                        color: gridColor
                    }
                },
                y: {
                    ticks: {
                        color: textColor
                    },
                    grid: {
                        color: gridColor
                    }
                }
            }
        },
        plugins: [{
            id: 'neonGlow',
            beforeDraw(chart) {
                const ctx = chart.ctx;
                ctx.save();
                ctx.shadowColor = primaryColor;
                ctx.shadowBlur = 20;
                ctx.restore();
            }
        }]
    });
}