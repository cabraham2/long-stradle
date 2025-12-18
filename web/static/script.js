// Global variables
let currentTickerInfo = null;
let currentSummary = null;
let currentScenarios = null;
let profitChart = null;
let volHistoryChart = null;
let volSensitivityChart = null;
let spotSensitivityChart = null;
let timeSensitivityChart = null;
let heatmapChart = null;
let comparisonChart = null;
let glossaryData = null;

// Theme Management
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update button text and icon
    document.getElementById('theme-icon').textContent = newTheme === 'dark' ? '🌙' : '☀️';
    document.getElementById('theme-text').textContent = newTheme === 'dark' ? 'Mode Clair' : 'Mode Sombre';
    
    // Update charts with new theme
    updateChartsTheme(newTheme);
}

// Load theme from localStorage
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.getElementById('theme-icon').textContent = savedTheme === 'dark' ? '🌙' : '☀️';
    document.getElementById('theme-text').textContent = savedTheme === 'dark' ? 'Mode Clair' : 'Mode Sombre';
}

// Load glossary data
async function loadGlossary() {
    try {
        const response = await fetch('/api/glossary');
        const data = await response.json();
        if (data.success) {
            glossaryData = data.glossary;
        }
    } catch (error) {
        console.error('Erreur chargement glossaire:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    loadGlossary();
});

// Update chart colors based on theme
function updateChartsTheme(theme) {
    const textColor = theme === 'dark' ? '#f1f5f9' : '#0f172a';
    const gridColor = theme === 'dark' ? '#334155' : '#e2e8f0';
    
    // Update all existing charts
    const charts = [profitChart, volHistoryChart, volSensitivityChart, 
                   spotSensitivityChart, timeSensitivityChart, heatmapChart, comparisonChart];
    
    charts.forEach(chart => {
        if (chart) {
            chart.options.scales.x.ticks.color = textColor;
            chart.options.scales.y.ticks.color = textColor;
            chart.options.scales.x.grid.color = gridColor;
            chart.options.scales.y.grid.color = gridColor;
            chart.update();
        }
    });
}

// Validate ticker
async function validateTicker() {
    const ticker = document.getElementById('ticker').value.trim().toUpperCase();
    const feedbackDiv = document.getElementById('ticker-feedback');
    const tickerInfoDiv = document.getElementById('ticker-info');
    const straddleParamsDiv = document.getElementById('straddle-params');
    
    if (!ticker) {
        showFeedback('Veuillez entrer un ticker', 'error');
        return;
    }
    
    feedbackDiv.innerHTML = '<div class="feedback-info">⏳ Validation en cours...</div>';
    
    try {
        const response = await fetch('/api/validate_ticker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ticker: ticker })
        });
        
        const data = await response.json();
        
        if (data.valid) {
            showFeedback(`✓ Ticker ${ticker} validé!`, 'success');
            currentTickerInfo = data.ticker_info;
            displayTickerInfo(data.ticker_info);
            tickerInfoDiv.style.display = 'block';
            straddleParamsDiv.style.display = 'block';
        } else {
            showFeedback(`✗ ${data.error}`, 'error');
            tickerInfoDiv.style.display = 'none';
            straddleParamsDiv.style.display = 'none';
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
    }
}

// Display ticker information
function displayTickerInfo(info) {
    document.getElementById('ticker-name').textContent = info.name;
    document.getElementById('ticker-symbol').textContent = info.ticker;
    
    // Current price
    const priceElement = document.getElementById('current-price');
    priceElement.textContent = `${info.currency} ${info.current_price.toFixed(2)}`;
    
    // Day change
    const changeElement = document.getElementById('day-change');
    const changeValue = info.day_change;
    const changePct = info.day_change_pct;
    const changeColor = changeValue >= 0 ? 'var(--success-color)' : 'var(--danger-color)';
    const changeSign = changeValue >= 0 ? '+' : '';
    
    changeElement.innerHTML = `<span style="color: ${changeColor}">${changeSign}${changeValue.toFixed(2)} (${changeSign}${changePct.toFixed(2)}%)</span>`;
    
    // Market cap
    document.getElementById('market-cap').textContent = info.market_cap_str;
    
    // Volume
    document.getElementById('volume').textContent = info.volume.toLocaleString();
}

// Calculate straddle
async function calculateStraddle() {
    if (!currentTickerInfo) {
        showFeedback('Veuillez d\'abord valider un ticker', 'error');
        return;
    }
    
    const ticker = currentTickerInfo.ticker;
    const days = document.getElementById('days').value;
    const strike = document.getElementById('strike').value;
    
    // Show loading
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    resultsSection.classList.add('loading');
    
    try {
        const response = await fetch('/api/calculate_straddle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ticker: ticker,
                days: days,
                strike: strike || null
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.summary, data.scenarios);
            saveCurrentData(data.summary, data.scenarios);
            resultsSection.classList.remove('loading');
            
            // Switch to basic tab and scroll
            showTab('basic');
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            showFeedback(`✗ Erreur: ${data.error}`, 'error');
            resultsSection.style.display = 'none';
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
        resultsSection.style.display = 'none';
    }
}

// Display results
function displayResults(summary, scenarios) {
    // Pricing
    document.getElementById('call-price').textContent = `$${summary.call_price.toFixed(2)}`;
    document.getElementById('put-price').textContent = `$${summary.put_price.toFixed(2)}`;
    document.getElementById('total-cost').textContent = `$${summary.total_cost.toFixed(2)}`;
    
    // Parameters
    document.getElementById('strike-value').textContent = `$${summary.strike.toFixed(2)}`;
    document.getElementById('expiry-value').textContent = `${summary.time_to_expiry_days} jours`;
    document.getElementById('volatility-value').textContent = `${(summary.volatility * 100).toFixed(2)}%`;
    document.getElementById('rate-value').textContent = `${(summary.risk_free_rate * 100).toFixed(2)}%`;
    
    // Risk/Reward
    document.getElementById('max-loss').textContent = `$${summary.max_loss.toFixed(2)}`;
    document.getElementById('max-profit').textContent = summary.max_profit;
    document.getElementById('lower-be').textContent = `$${summary.lower_break_even.toFixed(2)}`;
    document.getElementById('upper-be').textContent = `$${summary.upper_break_even.toFixed(2)}`;
    document.getElementById('required-move').textContent = `±${summary.break_even_move_pct.toFixed(2)}%`;
    
    // Greeks
    const greeks = summary.greeks;
    document.getElementById('delta').textContent = greeks.delta.toFixed(4);
    document.getElementById('gamma').textContent = greeks.gamma.toFixed(4);
    document.getElementById('vega').textContent = greeks.vega.toFixed(4);
    document.getElementById('theta').textContent = greeks.theta.toFixed(4);
    document.getElementById('rho').textContent = greeks.rho.toFixed(4);
    
    // Draw chart
    drawProfitChart(scenarios, summary.spot_price);
}

// Draw profit/loss chart
function drawProfitChart(scenarios, spotPrice) {
    const ctx = document.getElementById('profitChart').getContext('2d');
    
    // Destroy previous chart if exists
    if (profitChart) {
        profitChart.destroy();
    }
    
    // Prepare data
    const labels = scenarios.map(s => `${s.price_change_pct >= 0 ? '+' : ''}${s.price_change_pct}%`);
    const profits = scenarios.map(s => s.profit);
    
    // Color gradient
    const backgroundColors = profits.map(p => 
        p > 0 ? 'rgba(16, 185, 129, 0.6)' : 'rgba(239, 68, 68, 0.6)'
    );
    
    const borderColors = profits.map(p => 
        p > 0 ? 'rgba(16, 185, 129, 1)' : 'rgba(239, 68, 68, 1)'
    );
    
    profitChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Profit/Perte ($)',
                data: profits,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: backgroundColors,
                pointBorderColor: borderColors,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#f1f5f9',
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#f1f5f9',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            const profit = context.parsed.y;
                            const scenario = scenarios[context.dataIndex];
                            return [
                                `P&L: $${profit.toFixed(2)}`,
                                `Prix final: $${scenario.final_price.toFixed(2)}`,
                                `Payoff: $${scenario.payoff.toFixed(2)}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(51, 65, 85, 0.5)'
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(51, 65, 85, 0.5)'
                    },
                    ticks: {
                        color: '#94a3b8',
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

// Show feedback message
function showFeedback(message, type) {
    const feedbackDiv = document.getElementById('ticker-feedback');
    feedbackDiv.className = `feedback-${type}`;
    feedbackDiv.innerHTML = message;
}

// Tab management
function showTab(tabName) {
    // Hide all tabs
    const sections = ['results-section', 'advanced-section', 'compare-section', 
                     'monte-carlo-section', 'backtest-section', 'education-section',
                     'strategy-comparison-section'];
    sections.forEach(id => {
        const elem = document.getElementById(id);
        if (elem) elem.style.display = 'none';
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    const sectionMap = {
        'basic': 'results-section',
        'advanced': 'advanced-section',
        'compare': 'compare-section',
        'monte-carlo': 'monte-carlo-section',
        'backtest': 'backtest-section',
        'education': 'education-section'
    };
    
    const sectionId = sectionMap[tabName];
    if (sectionId) {
        const section = document.getElementById(sectionId);
        if (section) section.style.display = 'block';
        
        const btn = document.getElementById(`tab-${tabName}`);
        if (btn) btn.classList.add('active');
    }
    
    // Show multi-strategy comparison in compare tab
    if (tabName === 'compare' && currentTickerInfo) {
        const compSection = document.getElementById('strategy-comparison-section');
        if (compSection) compSection.style.display = 'block';
    }
}

// Loading overlay
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Volatility Analysis
async function loadVolatilityAnalysis() {
    if (!currentTickerInfo) return;
    
    showLoading();
    
    try {
        // Historical volatility
        const histResponse = await fetch(`/api/implied_volatility`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: currentTickerInfo.ticker })
        });
        
        const histData = await histResponse.json();
        
        if (histData.success) {
            drawVolatilityHistory(histData.volatility_data);
        }
        
        // Sensitivity to volatility
        const days = document.getElementById('days').value;
        const strike = document.getElementById('strike').value;
        
        const sensResponse = await fetch('/api/greeks_sensitivity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                days: days,
                strike: strike || null
            })
        });
        
        const sensData = await sensResponse.json();
        
        if (sensData.success) {
            drawVolatilitySensitivity(sensData.volatility_sensitivity);
            drawSpotSensitivity(sensData.spot_sensitivity);
            drawTimeSensitivity(sensData.time_sensitivity);
        }
        
        document.getElementById('vol-analysis-content').style.display = 'block';
        document.getElementById('greeks-analysis-content').style.display = 'block';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Erreur lors du chargement de l\'analyse');
    } finally {
        hideLoading();
    }
}

// Greeks Sensitivity
async function loadGreeksSensitivity() {
    await loadVolatilityAnalysis();
}

// Heatmap
async function loadHeatmap() {
    if (!currentTickerInfo) return;
    
    showLoading();
    
    try {
        const strike = document.getElementById('strike').value;
        
        const response = await fetch('/api/heatmap_data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                strike: strike || null
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            drawHeatmap(data.heatmap, data.days_range, data.price_changes);
            document.getElementById('heatmap-content').style.display = 'block';
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Erreur lors de la génération de la heatmap');
    } finally {
        hideLoading();
    }
}

// Comparison
async function loadComparison() {
    if (!currentTickerInfo) return;
    
    showLoading();
    
    try {
        const response = await fetch('/api/compare_strategies', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: currentTickerInfo.ticker })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayComparisonTable(data.comparisons);
            drawComparisonChart(data.comparisons);
            document.getElementById('comparison-results').style.display = 'block';
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Erreur lors de la comparaison');
    } finally {
        hideLoading();
    }
}

// Draw volatility history chart
function drawVolatilityHistory(volData) {
    const ctx = document.getElementById('volHistoryChart').getContext('2d');
    
    if (volHistoryChart) volHistoryChart.destroy();
    
    volHistoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: volData.map(v => v.period_label),
            datasets: [{
                label: 'Volatilité Historique (%)',
                data: volData.map(v => v.volatility),
                backgroundColor: 'rgba(59, 130, 246, 0.6)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#f1f5f9' } },
                title: {
                    display: true,
                    text: 'Volatilité Historique sur Différentes Périodes',
                    color: '#f1f5f9',
                    font: { size: 16 }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } }
            }
        }
    });
}

// Draw volatility sensitivity chart
function drawVolatilitySensitivity(volSens) {
    const ctx = document.getElementById('volSensitivityChart').getContext('2d');
    
    if (volSensitivityChart) volSensitivityChart.destroy();
    
    volSensitivityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: volSens.map(v => v.volatility.toFixed(1) + '%'),
            datasets: [{
                label: 'Prix du Straddle ($)',
                data: volSens.map(v => v.price),
                borderColor: 'rgba(16, 185, 129, 1)',
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#f1f5f9' } },
                title: {
                    display: true,
                    text: 'Sensibilité à la Volatilité',
                    color: '#f1f5f9',
                    font: { size: 16 }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } }
            }
        }
    });
}

// Draw spot sensitivity chart
function drawSpotSensitivity(spotSens) {
    const ctx = document.getElementById('spotSensitivityChart').getContext('2d');
    
    if (spotSensitivityChart) spotSensitivityChart.destroy();
    
    spotSensitivityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: spotSens.map(s => '$' + s.spot_price.toFixed(2)),
            datasets: [
                {
                    label: 'Prix du Straddle',
                    data: spotSens.map(s => s.price),
                    borderColor: 'rgba(139, 92, 246, 1)',
                    backgroundColor: 'rgba(139, 92, 246, 0.2)',
                    yAxisID: 'y',
                    borderWidth: 3,
                    tension: 0.4
                },
                {
                    label: 'Delta',
                    data: spotSens.map(s => s.delta),
                    borderColor: 'rgba(245, 158, 11, 1)',
                    backgroundColor: 'rgba(245, 158, 11, 0.2)',
                    yAxisID: 'y1',
                    borderWidth: 2,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { labels: { color: '#f1f5f9' } },
                title: {
                    display: true,
                    text: 'Sensibilité au Prix Spot',
                    color: '#f1f5f9',
                    font: { size: 16 }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8', maxRotation: 45 }, grid: { color: 'rgba(51, 65, 85, 0.5)' } },
                y: { type: 'linear', position: 'left', ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } },
                y1: { type: 'linear', position: 'right', ticks: { color: '#94a3b8' }, grid: { display: false } }
            }
        }
    });
}

// Draw time sensitivity chart
function drawTimeSensitivity(timeSens) {
    const ctx = document.getElementById('timeSensitivityChart').getContext('2d');
    
    if (timeSensitivityChart) timeSensitivityChart.destroy();
    
    timeSensitivityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeSens.map(t => t.days + 'j'),
            datasets: [{
                label: 'Prix du Straddle ($)',
                data: timeSens.map(t => t.price),
                borderColor: 'rgba(239, 68, 68, 1)',
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#f1f5f9' } },
                title: {
                    display: true,
                    text: 'Décroissance Temporelle (Theta)',
                    color: '#f1f5f9',
                    font: { size: 16 }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } }
            }
        }
    });
}

// Draw heatmap
function drawHeatmap(heatmapData, daysRange, priceChanges) {
    const ctx = document.getElementById('heatmapChart').getContext('2d');
    
    if (heatmapChart) heatmapChart.destroy();
    
    // Préparer les données pour une heatmap simulée avec line chart
    const datasets = daysRange.map((days, idx) => {
        const color = `hsl(${idx * 40}, 70%, 60%)`;
        return {
            label: `${days} jours`,
            data: heatmapData[idx].map(cell => cell.profit),
            borderColor: color,
            backgroundColor: color.replace(')', ', 0.2)').replace('hsl', 'hsla'),
            borderWidth: 2,
            tension: 0.4
        };
    });
    
    heatmapChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: priceChanges.map(p => p + '%'),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#f1f5f9' } },
                title: {
                    display: true,
                    text: 'Profit/Perte par Échéance et Variation de Prix',
                    color: '#f1f5f9',
                    font: { size: 16 }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } }
            }
        }
    });
}

// Display comparison table
function displayComparisonTable(comparisons) {
    const tbody = document.getElementById('comparisonBody');
    tbody.innerHTML = '';
    
    comparisons.forEach(comp => {
        const row = document.createElement('tr');
        
        const costClass = comp.cost < 5 ? 'positive' : comp.cost > 15 ? 'negative' : '';
        const moveClass = comp.break_even_move < 5 ? 'positive' : comp.break_even_move > 15 ? 'negative' : '';
        
        row.innerHTML = `
            <td><strong>${comp.days} jours</strong></td>
            <td>${comp.strike_type}</td>
            <td class="${costClass}">$${comp.cost.toFixed(2)}</td>
            <td class="${moveClass}">±${comp.break_even_move.toFixed(2)}%</td>
            <td class="negative">$${comp.theta.toFixed(4)}</td>
            <td class="positive">${comp.vega.toFixed(4)}</td>
        `;
        
        tbody.appendChild(row);
    });
}

// Draw comparison chart
function drawComparisonChart(comparisons) {
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    
    if (comparisonChart) comparisonChart.destroy();
    
    // Grouper par échéance
    const dayGroups = [...new Set(comparisons.map(c => c.days))];
    
    const datasets = dayGroups.map((days, idx) => {
        const filtered = comparisons.filter(c => c.days === days);
        const color = `hsl(${idx * 50}, 70%, 60%)`;
        
        return {
            label: `${days} jours`,
            data: filtered.map(c => c.cost),
            backgroundColor: color,
            borderColor: color,
            borderWidth: 2
        };
    });
    
    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['ATM', '+5%', '-5%'],
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#f1f5f9' } },
                title: {
                    display: true,
                    text: 'Coût du Straddle par Échéance et Strike',
                    color: '#f1f5f9',
                    font: { size: 16 }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.5)' } }
            }
        }
    });
}

// Export functions
async function exportToJSON() {
    if (!currentSummary) {
        alert('Aucune analyse à exporter');
        return;
    }
    
    const data = {
        ticker: currentTickerInfo.ticker,
        summary: currentSummary,
        scenarios: currentScenarios,
        timestamp: new Date().toISOString()
    };
    
    await fetch('/api/export_json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `straddle_${currentTickerInfo.ticker}_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
}

function printReport() {
    window.print();
}

function shareAnalysis() {
    if (navigator.share && currentSummary) {
        navigator.share({
            title: `Analyse Long Straddle - ${currentTickerInfo.ticker}`,
            text: `Coût: $${currentSummary.total_cost.toFixed(2)}, Mouvement requis: ±${currentSummary.break_even_move_pct.toFixed(2)}%`,
            url: window.location.href
        });
    } else {
        alert('Partage non supporté sur ce navigateur');
    }
}

function resetAnalysis() {
    if (confirm('Voulez-vous recommencer une nouvelle analyse?')) {
        location.reload();
    }
}

function showAbout() {
    alert('Options Pricer v1.0\n\nPriceur d\'options Long Straddle utilisant le modèle Black-Scholes.\n\nDéveloppé avec Python, Flask et Chart.js');
}

// Enter key support
document.getElementById('ticker').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        validateTicker();
    }
});

// Save current data for export
function saveCurrentData(summary, scenarios) {
    currentSummary = summary;
    currentScenarios = scenarios;
    document.getElementById('actions-section').style.display = 'block';
}

// Export functions
async function exportToPDF() {
    if (!currentSummary || !currentTickerInfo) {
        showFeedback('Aucune donnée à exporter. Calculez d\'abord un straddle.', 'error');
        return;
    }
    
    showFeedback('⏳ Génération du PDF en cours...', 'info');
    
    try {
        const response = await fetch('/api/export_pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                summary: currentSummary,
                scenarios: currentScenarios
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `straddle_${currentTickerInfo.ticker}_${new Date().toISOString().slice(0,10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showFeedback('✓ PDF téléchargé avec succès!', 'success');
        } else {
            const error = await response.json();
            showFeedback(`✗ Erreur: ${error.error}`, 'error');
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
    }
}

async function exportToExcel() {
    if (!currentSummary || !currentTickerInfo) {
        showFeedback('Aucune donnée à exporter. Calculez d\'abord un straddle.', 'error');
        return;
    }
    
    showFeedback('⏳ Génération du fichier Excel en cours...', 'info');
    
    try {
        const response = await fetch('/api/export_excel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                summary: currentSummary,
                scenarios: currentScenarios
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `straddle_${currentTickerInfo.ticker}_${new Date().toISOString().slice(0,10)}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showFeedback('✓ Excel téléchargé avec succès!', 'success');
        } else {
            const error = await response.json();
            showFeedback(`✗ Erreur: ${error.error}`, 'error');
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
    }
}

async function exportToCSV() {
    if (!currentScenarios || !currentTickerInfo) {
        showFeedback('Aucune donnée à exporter. Calculez d\'abord un straddle.', 'error');
        return;
    }
    
    showFeedback('⏳ Génération du CSV en cours...', 'info');
    
    try {
        const response = await fetch('/api/export_csv', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                scenarios: currentScenarios
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scenarios_${currentTickerInfo.ticker}_${new Date().toISOString().slice(0,10)}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showFeedback('✓ CSV téléchargé avec succès!', 'success');
        } else {
            const error = await response.json();
            showFeedback(`✗ Erreur: ${error.error}`, 'error');
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
    }
}

// Multi-strategy comparison
async function compareStrategies() {
    if (!currentTickerInfo) {
        showFeedback('Validez d\'abord un ticker', 'error');
        return;
    }
    
    const days = document.getElementById('days').value;
    showFeedback('⏳ Comparaison des stratégies en cours...', 'info');
    
    try {
        const response = await fetch('/api/compare_multi_strategies', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                days: days
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayStrategyComparison(data.strategies);
            showFeedback('✓ Comparaison générée!', 'success');
        } else {
            showFeedback(`✗ Erreur: ${data.error}`, 'error');
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
    }
}

function displayStrategyComparison(strategies) {
    const container = document.getElementById('strategy-comparison-results');
    
    // Create comparison table
    let html = '<div class="comparison-grid">';
    
    const strategyNames = {
        'straddle': 'Long Straddle',
        'strangle': 'Long Strangle',
        'iron_condor': 'Iron Condor'
    };
    
    for (const [key, strategy] of Object.entries(strategies)) {
        if (key === 'price_range' || key === 'spot_price') continue;
        
        html += `
            <div class="strategy-card">
                <h4>${strategyNames[key] || key}</h4>
                <div class="strategy-details">
                    <p><strong>Coût:</strong> $${strategy.summary.total_cost?.toFixed(2) || strategy.summary.net_credit?.toFixed(2) || 'N/A'}</p>
                    <p><strong>Profit Max:</strong> ${strategy.summary.max_profit}</p>
                    <p><strong>Perte Max:</strong> $${strategy.summary.max_loss?.toFixed(2) || 'N/A'}</p>
                    <p><strong>Break-Even Inf:</strong> $${strategy.summary.lower_break_even?.toFixed(2)}</p>
                    <p><strong>Break-Even Sup:</strong> $${strategy.summary.upper_break_even?.toFixed(2)}</p>
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    container.innerHTML = html;
    
    // Draw comparison chart
    drawComparisonChart(strategies);
}

function drawComparisonChart(strategies) {
    const canvas = document.getElementById('comparison-chart');
    const ctx = canvas.getContext('2d');
    
    if (comparisonChart) {
        comparisonChart.destroy();
    }
    
    const theme = document.documentElement.getAttribute('data-theme');
    const textColor = theme === 'dark' ? '#f1f5f9' : '#0f172a';
    const gridColor = theme === 'dark' ? '#334155' : '#e2e8f0';
    
    const datasets = [];
    const colors = {
        'straddle': '#3b82f6',
        'strangle': '#8b5cf6',
        'iron_condor': '#10b981'
    };
    
    for (const [key, strategy] of Object.entries(strategies)) {
        if (key === 'price_range' || key === 'spot_price') continue;
        
        datasets.push({
            label: key.replace('_', ' ').toUpperCase(),
            data: strategy.payoffs,
            borderColor: colors[key],
            backgroundColor: colors[key] + '20',
            borderWidth: 2,
            tension: 0.4
        });
    }
    
    comparisonChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: strategies.price_range,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Comparaison P&L à l\'Expiration',
                    color: textColor
                },
                legend: {
                    labels: { color: textColor }
                },
                zoom: {
                    zoom: {
                        wheel: { enabled: true },
                        pinch: { enabled: true },
                        mode: 'xy',
                    },
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Prix du Sous-Jacent ($)', color: textColor },
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    title: { display: true, text: 'Profit/Perte ($)', color: textColor },
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

// Monte Carlo Analysis
async function runMonteCarloAnalysis() {
    if (!currentTickerInfo) {
        showFeedback('Validez d\'abord un ticker', 'error');
        return;
    }
    
    const days = document.getElementById('days').value;
    const strategy = document.getElementById('mc-strategy')?.value || 'straddle';
    const simulations = document.getElementById('mc-simulations')?.value || 10000;
    
    showFeedback('⏳ Simulation Monte Carlo en cours...', 'info');
    
    try {
        const response = await fetch('/api/monte_carlo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                days: days,
                strategy: strategy,
                simulations: simulations
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayMonteCarloResults(data);
            showFeedback('✓ Analyse Monte Carlo terminée!', 'success');
        } else {
            showFeedback(`✗ Erreur: ${data.error}`, 'error');
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
    }
}

function displayMonteCarloResults(data) {
    const container = document.getElementById('monte-carlo-results');
    const mc = data.monte_carlo;
    const var_data = data.value_at_risk;
    const be = data.breakeven_analysis;
    
    const html = `
        <div class="mc-results-grid">
            <div class="mc-card">
                <h4>📊 Probabilités</h4>
                <p><strong>Prob. de Profit:</strong> ${(mc.probability_of_profit * 100).toFixed(2)}%</p>
                <p><strong>Prob. de Perte:</strong> ${(mc.probability_of_loss * 100).toFixed(2)}%</p>
                <p><strong>Espérance de Gain:</strong> $${mc.expected_profit.toFixed(2)}</p>
            </div>
            
            <div class="mc-card">
                <h4>💰 Value at Risk (95%)</h4>
                <p><strong>VaR:</strong> $${var_data.value_at_risk.toFixed(2)}</p>
                <p><strong>CVaR:</strong> $${var_data.conditional_var.toFixed(2)}</p>
                <p class="mc-interpretation">${var_data.interpretation}</p>
            </div>
            
            <div class="mc-card">
                <h4>🎯 Break-Even</h4>
                <p><strong>Prob. < BE Inf:</strong> ${(be.prob_below_lower_be * 100).toFixed(2)}%</p>
                <p><strong>Prob. > BE Sup:</strong> ${(be.prob_above_upper_be * 100).toFixed(2)}%</p>
                <p><strong>Prob. Profitable:</strong> ${(be.prob_profitable * 100).toFixed(2)}%</p>
            </div>
            
            <div class="mc-card">
                <h4>📈 Statistiques</h4>
                <p><strong>Médiane:</strong> $${mc.median_profit.toFixed(2)}</p>
                <p><strong>Écart-type:</strong> $${mc.std_profit.toFixed(2)}</p>
                <p><strong>Ratio R/R:</strong> ${mc.risk_reward_ratio.toFixed(2)}</p>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

// Backtesting
async function runBacktest() {
    if (!currentTickerInfo) {
        showFeedback('Validez d\'abord un ticker', 'error');
        return;
    }
    
    const strategy = document.getElementById('backtest-strategy')?.value || 'straddle';
    const holdingDays = document.getElementById('backtest-days')?.value || 30;
    
    showFeedback('⏳ Backtesting en cours (peut prendre quelques secondes)...', 'info');
    
    try {
        const response = await fetch('/api/backtest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: currentTickerInfo.ticker,
                strategy: strategy,
                holding_days: holdingDays
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayBacktestResults(data);
            showFeedback('✓ Backtest terminé!', 'success');
        } else {
            showFeedback(`✗ Erreur: ${data.error}`, 'error');
        }
    } catch (error) {
        showFeedback(`✗ Erreur: ${error.message}`, 'error');
    }
}

function displayBacktestResults(data) {
    const container = document.getElementById('backtest-results');
    
    const html = `
        <div class="backtest-summary">
            <h3>Résultats du Backtest - ${data.strategy}</h3>
            <p class="backtest-period">${data.period}</p>
            
            <div class="backtest-grid">
                <div class="backtest-stat">
                    <span class="stat-label">Total Trades</span>
                    <span class="stat-value">${data.total_trades}</span>
                </div>
                <div class="backtest-stat">
                    <span class="stat-label">Taux de Réussite</span>
                    <span class="stat-value">${data.win_rate.toFixed(2)}%</span>
                </div>
                <div class="backtest-stat">
                    <span class="stat-label">Profit Total</span>
                    <span class="stat-value ${data.total_profit >= 0 ? 'positive' : 'negative'}">
                        $${data.total_profit.toFixed(2)}
                    </span>
                </div>
                <div class="backtest-stat">
                    <span class="stat-label">Profit Moyen</span>
                    <span class="stat-value">$${data.avg_profit_per_trade.toFixed(2)}</span>
                </div>
                <div class="backtest-stat">
                    <span class="stat-label">Profit Factor</span>
                    <span class="stat-value">${data.profit_factor.toFixed(2)}</span>
                </div>
                <div class="backtest-stat">
                    <span class="stat-label">Sharpe Ratio</span>
                    <span class="stat-value">${data.sharpe_ratio.toFixed(2)}</span>
                </div>
                <div class="backtest-stat">
                    <span class="stat-label">Max Drawdown</span>
                    <span class="stat-value negative">$${data.max_drawdown.toFixed(2)}</span>
                </div>
                <div class="backtest-stat">
                    <span class="stat-label">Meilleur Trade</span>
                    <span class="stat-value positive">$${data.best_trade.toFixed(2)}</span>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}
