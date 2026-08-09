/* ==========================================================================
   DATA ANALYTICS PORTFOLIO INTERACTIVE LOGIC & SIMULATORS
   Author: Rutuja Shinde
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initCounters();
    initSQLPlayground();
    initPowerBIDashboard();
    initNavScroll();
});

/* --------------------------------------------------------------------------
   1. Live Counter Animations
   -------------------------------------------------------------------------- */
function initCounters() {
    const kpiValues = document.querySelectorAll('.kpi-value');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                const isCurrency = entry.target.id.includes('revenue') || entry.target.id.includes('leak');
                animateValue(entry.target, 0, target, 1500, isCurrency);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    kpiValues.forEach(val => observer.observe(val));
}

function animateValue(obj, start, end, duration, isCurrency) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        
        if (isCurrency) {
            obj.innerHTML = '$' + current.toLocaleString();
        } else {
            obj.innerHTML = current.toLocaleString();
        }
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

/* --------------------------------------------------------------------------
   2. Project 1: Data Audit Widget State Toggle
   -------------------------------------------------------------------------- */
const auditData = {
    raw: {
        rows: '1,200',
        missing: '42 (CouponCode)',
        priceErr: '8 Mismatches',
        status: 'Raw Unchecked',
        missingClass: 'warning-text',
        priceClass: 'danger-text',
        statusClass: 'warning-text',
        code: `# Raw Dataset Loading & Audit
import pandas as pd
df = pd.read_csv("Dataset for Data Analytics - Sheet1.csv")

# Identify raw issues
print("Missing CouponCodes:", df['CouponCode'].isnull().sum()) # 42 missing
print("Row Count:", len(df))
print("Price Errors (TotalPrice != Quantity * UnitPrice)")`
    },
    clean: {
        rows: '1,200',
        missing: '0 (Cleaned)',
        priceErr: '0 Mismatches',
        status: 'Normalized 100%',
        missingClass: 'success-text',
        priceClass: 'success-text',
        statusClass: 'success-text',
        code: `# Step 3c: Verify & Correct TotalPrice = Quantity * UnitPrice
df['Calculated_Total'] = df['Quantity'] * df['UnitPrice']
df['Price_Diff'] = abs(df['TotalPrice'] - df['Calculated_Total'])

# Impute missing CouponCode with 'NoCoupon'
df['CouponCode'] = df['CouponCode'].fillna('NoCoupon')

# Recalculate TotalPrice where discrepancies exist
df.loc[df['Price_Diff'] > 0.01, 'TotalPrice'] = df['Calculated_Total']`
    }
};

function setAuditState(state) {
    const btnRaw = document.getElementById('btn-raw-data');
    const btnClean = document.getElementById('btn-clean-data');
    const rowsEl = document.getElementById('audit-rows');
    const missingEl = document.getElementById('audit-missing');
    const priceEl = document.getElementById('audit-price-err');
    const statusEl = document.getElementById('audit-status');
    const codeEl = document.getElementById('code-snippet');

    if (state === 'raw') {
        btnRaw.classList.add('active');
        btnClean.classList.remove('active');
        const data = auditData.raw;
        rowsEl.textContent = data.rows;
        missingEl.textContent = data.missing;
        missingEl.className = 'metric-val ' + data.missingClass;
        priceEl.textContent = data.priceErr;
        priceEl.className = 'metric-val ' + data.priceClass;
        statusEl.textContent = data.status;
        statusEl.className = 'metric-val ' + data.statusClass;
        codeEl.textContent = data.code;
    } else {
        btnClean.classList.add('active');
        btnRaw.classList.remove('active');
        const data = auditData.clean;
        rowsEl.textContent = data.rows;
        missingEl.textContent = data.missing;
        missingEl.className = 'metric-val ' + data.missingClass;
        priceEl.textContent = data.priceErr;
        priceEl.className = 'metric-val ' + data.priceClass;
        statusEl.textContent = data.status;
        statusEl.className = 'metric-val ' + data.statusClass;
        codeEl.textContent = data.code;
    }
}

function copyCodeSnippet() {
    const code = document.getElementById('code-snippet').textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert('Python snippet copied to clipboard!');
    });
}

/* --------------------------------------------------------------------------
   3. Project 2: Chart Lightbox Modal
   -------------------------------------------------------------------------- */
function openChartModal(imgSrc, title, desc) {
    const modal = document.getElementById('chartModal');
    const modalImg = document.getElementById('modal-img');
    const modalTitle = document.getElementById('modal-title');
    const modalDesc = document.getElementById('modal-desc');

    modalImg.src = imgSrc;
    modalTitle.textContent = title;
    modalDesc.textContent = desc;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeChartModal() {
    const modal = document.getElementById('chartModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

/* --------------------------------------------------------------------------
   4. Project 3: SQL Playground Simulator
   -------------------------------------------------------------------------- */
const sqlQueries = {
    high_value: {
        sql: `SELECT OrderID, Product, Quantity, UnitPrice, TotalPrice, OrderStatus 
FROM orders 
WHERE TotalPrice > 2000 
ORDER BY TotalPrice DESC 
LIMIT 10;`,
        headers: ['OrderID', 'Product', 'Quantity', 'UnitPrice', 'TotalPrice', 'OrderStatus'],
        rows: [
            ['ORD200789', 'Tablet', 5, '$691.28', '$3,456.40', '<span class="text-emerald">Delivered</span>'],
            ['ORD201122', 'Monitor', 5, '$678.19', '$3,390.95', '<span class="text-cyan">Shipped</span>'],
            ['ORD200632', 'Laptop', 5, '$678.16', '$3,390.80', '<span class="text-rose">Cancelled</span>'],
            ['ORD200469', 'Chair', 5, '$676.98', '$3,384.90', '<span class="text-amber">Returned</span>'],
            ['ORD200328', 'Tablet', 5, '$674.04', '$3,370.20', '<span class="text-emerald">Delivered</span>'],
            ['ORD200107', 'Printer', 5, '$670.75', '$3,353.75', '<span class="text-cyan">Shipped</span>'],
            ['ORD200326', 'Laptop', 5, '$670.48', '$3,352.40', '<span class="text-emerald">Delivered</span>'],
            ['ORD201065', 'Printer', 5, '$666.80', '$3,334.00', '<span class="text-rose">Cancelled</span>'],
            ['ORD201031', 'Phone', 5, '$664.51', '$3,322.55', '<span class="text-amber">Returned</span>'],
            ['ORD200463', 'Laptop', 5, '$662.78', '$3,313.90', '<span class="text-emerald">Delivered</span>']
        ]
    },
    status_summary: {
        sql: `SELECT OrderStatus, COUNT(*) AS OrderCount, SUM(TotalPrice) AS Revenue, AVG(TotalPrice) AS AvgOrderValue 
FROM orders 
GROUP BY OrderStatus 
ORDER BY Revenue DESC;`,
        headers: ['OrderStatus', 'OrderCount', 'Total Revenue ($)', 'Avg Order Value ($)'],
        rows: [
            ['<span class="text-emerald">Delivered</span>', '357', '$375,400.00', '$1,051.54'],
            ['<span class="text-cyan">Shipped</span>', '348', '$365,685.00', '$1,050.82'],
            ['<span class="text-rose">Cancelled</span>', '249', '$261,300.00', '$1,049.40'],
            ['<span class="text-amber">Returned</span>', '246', '$258,400.00', '$1,050.41']
        ]
    },
    product_rev: {
        sql: `SELECT Product, COUNT(OrderID) as TotalOrders, SUM(TotalPrice) as Revenue, AVG(UnitPrice) as AvgPrice 
FROM orders 
GROUP BY Product 
ORDER BY Revenue DESC;`,
        headers: ['Product', 'TotalOrders', 'Total Revenue ($)', 'Avg Unit Price ($)'],
        rows: [
            ['Monitor', '182', '$195,430.00', '$412.50'],
            ['Laptop', '178', '$192,150.00', '$620.10'],
            ['Phone', '174', '$185,900.00', '$380.40'],
            ['Printer', '169', '$178,200.00', '$440.00'],
            ['Tablet', '168', '$175,800.00', '$390.20'],
            ['Desk', '165', '$169,400.00', '$310.80'],
            ['Chair', '164', '$163,905.00', '$280.50']
        ]
    },
    payment_method: {
        sql: `SELECT PaymentMethod, COUNT(*) AS Orders, SUM(TotalPrice) AS TotalRevenue, AVG(TotalPrice) AS AOV 
FROM orders 
GROUP BY PaymentMethod 
ORDER BY TotalRevenue DESC;`,
        headers: ['PaymentMethod', 'Orders', 'Total Revenue ($)', 'Average Order ($)'],
        rows: [
            ['Credit Card', '258', '$272,400.00', '$1,055.81'],
            ['Online', '245', '$258,900.00', '$1,056.73'],
            ['Debit Card', '238', '$249,800.00', '$1,049.58'],
            ['Cash', '231', '$241,500.00', '$1,045.45'],
            ['Gift Card', '228', '$238,185.00', '$1,044.67']
        ]
    }
};

let currentQueryKey = 'high_value';

function initSQLPlayground() {
    renderSQLOutput('high_value');
}

function runPresetQuery(key) {
    currentQueryKey = key;
    const btns = document.querySelectorAll('.sql-preset-btn');
    btns.forEach(btn => btn.classList.remove('active'));
    
    // Highlight active button
    event.target.classList.add('active');

    const queryData = sqlQueries[key];
    document.getElementById('sql-query-input').value = queryData.sql;
    renderSQLOutput(key);
}

function executeCurrentQuery() {
    renderSQLOutput(currentQueryKey);
}

function renderSQLOutput(key) {
    const data = sqlQueries[key];
    const table = document.getElementById('sql-output-table');
    const countEl = document.getElementById('sql-row-count');

    // Headers
    let headerHTML = '<tr>';
    data.headers.forEach(h => {
        headerHTML += `<th>${h}</th>`;
    });
    headerHTML += '</tr>';
    table.querySelector('thead').innerHTML = headerHTML;

    // Rows
    let rowsHTML = '';
    data.rows.forEach(r => {
        rowsHTML += '<tr>';
        r.forEach(cell => {
            rowsHTML += `<td>${cell}</td>`;
        });
        rowsHTML += '</tr>';
    });
    table.querySelector('tbody').innerHTML = rowsHTML;

    countEl.textContent = `Showing ${data.rows.length} records`;
}

/* --------------------------------------------------------------------------
   5. Project 4: Simulated Power BI Executive Dashboard State
   -------------------------------------------------------------------------- */
const pbiData = {
    All: {
        rev: '$1,260,785',
        orders: '1,200',
        aov: '$1,050.65',
        leak: '41.09%',
        bars: [
            { label: 'Monitor', val: '$195.4k', pct: 100, color: '#38BDF8' },
            { label: 'Laptop', val: '$192.1k', pct: 98, color: '#818CF8' },
            { label: 'Phone', val: '$185.9k', pct: 95, color: '#10B981' },
            { label: 'Printer', val: '$178.2k', pct: 91, color: '#F59E0B' },
            { label: 'Tablet', val: '$175.8k', pct: 90, color: '#EC4899' },
            { label: 'Desk', val: '$169.4k', pct: 86, color: '#6366F1' },
            { label: 'Chair', val: '$163.9k', pct: 83, color: '#14B8A6' }
        ]
    },
    Monitor: {
        rev: '$195,430',
        orders: '182',
        aov: '$1,073.79',
        leak: '39.56%',
        bars: [
            { label: 'Delivered', val: '$62.5k', pct: 100, color: '#10B981' },
            { label: 'Shipped', val: '$55.6k', pct: 88, color: '#38BDF8' },
            { label: 'Cancelled', val: '$39.2k', pct: 62, color: '#F43F5E' },
            { label: 'Returned', val: '$38.1k', pct: 60, color: '#F59E0B' }
        ]
    },
    Laptop: {
        rev: '$192,150',
        orders: '178',
        aov: '$1,079.49',
        leak: '42.13%',
        bars: [
            { label: 'Delivered', val: '$58.1k', pct: 100, color: '#10B981' },
            { label: 'Shipped', val: '$53.1k', pct: 91, color: '#38BDF8' },
            { label: 'Cancelled', val: '$41.8k', pct: 72, color: '#F43F5E' },
            { label: 'Returned', val: '$39.1k', pct: 67, color: '#F59E0B' }
        ]
    },
    Delivered: {
        rev: '$375,400',
        orders: '357',
        aov: '$1,051.54',
        leak: '0.00%',
        bars: [
            { label: 'Monitor', val: '$62.5k', pct: 100, color: '#38BDF8' },
            { label: 'Laptop', val: '$58.1k', pct: 93, color: '#818CF8' },
            { label: 'Phone', val: '$55.4k', pct: 88, color: '#10B981' },
            { label: 'Printer', val: '$52.9k', pct: 84, color: '#F59E0B' },
            { label: 'Tablet', val: '$51.2k', pct: 81, color: '#EC4899' }
        ]
    },
    Cancelled: {
        rev: '$261,300',
        orders: '249',
        aov: '$1,049.40',
        leak: '100.00%',
        bars: [
            { label: 'Laptop', val: '$41.8k', pct: 100, color: '#F43F5E' },
            { label: 'Monitor', val: '$39.2k', pct: 93, color: '#F43F5E' },
            { label: 'Phone', val: '$38.5k', pct: 92, color: '#F43F5E' },
            { label: 'Tablet', val: '$36.9k', pct: 88, color: '#F43F5E' }
        ]
    }
};

function initPowerBIDashboard() {
    renderPowerBIState('All');
}

function updatePowerBIDashboard() {
    const prodSelect = document.getElementById('pbi-product-select').value;
    const statusSelect = document.getElementById('pbi-status-select').value;

    let key = 'All';
    if (statusSelect !== 'All') {
        key = statusSelect;
    } else if (prodSelect !== 'All') {
        key = prodSelect;
    }

    renderPowerBIState(key);
}

function renderPowerBIState(key) {
    const data = pbiData[key] || pbiData['All'];
    
    document.getElementById('pbi-kpi-rev').textContent = data.rev;
    document.getElementById('pbi-kpi-orders').textContent = data.orders;
    document.getElementById('pbi-kpi-aov').textContent = data.aov;
    document.getElementById('pbi-kpi-leak').textContent = data.leak;

    // Render Bars
    const barChartContainer = document.getElementById('pbi-bar-chart');
    let barsHTML = '';
    data.bars.forEach(b => {
        barsHTML += `
        <div class="pbi-bar-row">
            <span class="pbi-bar-label">${b.label}</span>
            <div class="pbi-bar-track">
                <div class="pbi-bar-value" style="width: ${b.pct}%; background-color: ${b.color};">
                    ${b.val}
                </div>
            </div>
        </div>`;
    });
    barChartContainer.innerHTML = barsHTML;

    // Render Donut Chart SVG
    const donutContainer = document.getElementById('pbi-donut-chart');
    donutContainer.innerHTML = `
    <svg width="160" height="160" viewBox="0 0 42 42" class="donut-svg">
        <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#1E293B" stroke-width="5"></circle>
        <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#10B981" stroke-width="5" stroke-dasharray="29.7 70.3" stroke-dashoffset="0"></circle>
        <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#38BDF8" stroke-width="5" stroke-dasharray="29.1 70.9" stroke-dashoffset="-29.7"></circle>
        <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#F43F5E" stroke-width="5" stroke-dasharray="20.7 79.3" stroke-dashoffset="-58.8"></circle>
        <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#F59E0B" stroke-width="5" stroke-dasharray="20.5 79.5" stroke-dashoffset="-79.5"></circle>
    </svg>`;
}

/* --------------------------------------------------------------------------
   6. Navigation Active Link Update on Scroll
   -------------------------------------------------------------------------- */
function initNavScroll() {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 120;
            if (window.scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}
