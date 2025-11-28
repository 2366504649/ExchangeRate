// Global state
let currentCurrency = 'USD';
let rateChart = null;
let invertRate = false;

document.addEventListener('DOMContentLoaded', () => {
    initChart();
    setupEventListeners();
    fetchData();
    updateDate();
});

function updateDate() {
    const dateElement = document.getElementById('current-date');
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateElement.textContent = new Date().toLocaleDateString('en-US', options);
}

function setupEventListeners() {
    // Sidebar Navigation
    const navItems = document.querySelectorAll('#currency-list li');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // Remove active class from all
            navItems.forEach(li => li.classList.remove('active'));
            // Add active to clicked
            const target = e.currentTarget;
            target.classList.add('active');

            // Update state
            currentCurrency = target.dataset.currency;

            // Update UI
            updateTitle();
            fetchData();
        });
    });

    // Toggle Switch
    const toggle = document.getElementById('rate-toggle');
    toggle.addEventListener('change', (e) => {
        invertRate = e.target.checked;
        fetchData();
    });
}

function updateTitle() {
    const titleElement = document.getElementById('current-view-title');
    const currencyNames = {
        'USD': 'US Dollar',
        'JPY': 'Japanese Yen',
        'THB': 'Thai Baht',
        'MYR': 'Malaysian Ringgit',
        'SGD': 'Singapore Dollar',
        'PHP': 'Philippine Peso'
    };
    titleElement.textContent = `${currentCurrency} - ${currencyNames[currentCurrency]} Trend`;
}

function initChart() {
    const ctx = document.getElementById('rateChart').getContext('2d');

    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(52, 152, 219, 0.5)'); // Start color
    gradient.addColorStop(1, 'rgba(52, 152, 219, 0.0)'); // End color

    rateChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Exchange Rate',
                data: [],
                borderColor: '#3498db',
                backgroundColor: gradient,
                borderWidth: 3,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#3498db',
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(44, 62, 80, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return `Rate: ${context.parsed.y.toFixed(4)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#7f8c8d'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(0,0,0,0.05)'
                    },
                    ticks: {
                        color: '#7f8c8d'
                    }
                }
            }
        }
    });
}

async function fetchData() {
    try {
        // Fetch History
        const historyResponse = await fetch(`/api/history?currency=${currentCurrency}`);
        const historyData = await historyResponse.json();
        updateChart(historyData);

        // Fetch Summary
        const summaryResponse = await fetch('/api/summary');
        const summaryData = await summaryResponse.json();
        updateSummary(summaryData);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateChart(data) {
    const labels = data.map(item => item.date);
    let rates = data.map(item => item.rate);

    if (invertRate) {
        // Assuming raw rate is CNY per 100 units.
        // Inverted: Units per 1 CNY = 100 / Rate
        // Or if we want 1 Unit -> CNY, it's Rate / 100.
        // Let's stick to:
        // Default (False): Rate / 100 (Price of 1 Unit in CNY)
        // Inverted (True): 100 / Rate (Price of 1 CNY in Units)? No, that's confusing.

        // Let's do:
        // Default: 1 Foreign Unit = X CNY (Rate / 100)
        // Inverted: 1 CNY = X Foreign Units (100 / Rate)

        rates = rates.map(r => r ? (100 / r) : null);
    } else {
        rates = rates.map(r => r ? (r / 100) : null);
    }

    rateChart.data.labels = labels;
    rateChart.data.datasets[0].data = rates;
    rateChart.update();
}

function updateSummary(data) {
    const container = document.getElementById('summary-container');
    container.innerHTML = '';

    data.forEach(item => {
        if (typeof item === 'string') return; // Skip error messages for now

        const isUp = item.trend === 'up';
        const trendClass = isUp ? 'trend-up' : 'trend-down';
        const arrowIcon = isUp ? 'fa-arrow-trend-up' : 'fa-arrow-trend-down';
        const sign = isUp ? '+' : '';

        // Calculate display rate
        let displayRate = item.current;
        if (invertRate) {
            displayRate = displayRate ? (100 / displayRate) : 0;
        } else {
            displayRate = displayRate ? (displayRate / 100) : 0;
        }

        const card = document.createElement('div');
        card.className = `summary-card ${trendClass}`;
        card.innerHTML = `
            <div class="currency-info">
                <h4>
                    <span class="flag-icon">${getFlag(item.currency)}</span>
                    ${item.currency}
                </h4>
                <div class="rate">${displayRate.toFixed(4)}</div>
            </div>
            <div class="trend-info">
                <div class="percent-change">
                    <i class="fa-solid ${arrowIcon}"></i>
                    ${sign}${item.percent}%
                </div>
                <div class="suggestion-text">${item.suggestion}</div>
            </div>
        `;

        // Add click event to switch view
        card.style.cursor = 'pointer';
        card.addEventListener('click', () => {
            currentCurrency = item.currency;
            updateTitle();
            fetchData();

            // Update sidebar active state
            document.querySelectorAll('#currency-list li').forEach(li => {
                li.classList.remove('active');
                if (li.dataset.currency === item.currency) {
                    li.classList.add('active');
                }
            });
        });

        container.appendChild(card);
    });
}

function getFlag(currency) {
    const flags = {
        'USD': '🇺🇸',
        'JPY': '🇯🇵',
        'THB': '🇹🇭',
        'MYR': '🇲🇾',
        'SGD': '🇸🇬',
        'PHP': '🇵🇭'
    };
    return flags[currency] || '🏳️';
}
