$(document).ready(function() {
    // 通用加载动画HTML
    const loadingHtml = `
        <div class="loading-overlay">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <div class="mt-2">处理中，请稍候...</div>
        </div>
    `;

    // 添加加载动画的CSS
    $('head').append(`
        <style>
            .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            }
        </style>
    `);

    // 显示加载动画
    function showLoading() {
        $('body').append(loadingHtml);
    }

    // 隐藏加载动画
    function hideLoading() {
        $('.loading-overlay').remove();
    }

    // 漏洞扫描功能
    $('#scanButton').click(function() {
        showLoading();
        $(this).prop('disabled', true);

        setTimeout(function() {
            $.ajax({
                url: '/api/scan',
                method: 'POST',
                success: function(response) {
                    $('#scanResults').empty();
                    response.forEach(function(vuln) {
                        $('#scanResults').append(`
                            <div class="alert alert-warning">
                                <h5>${vuln.name}</h5>
                                <p>${vuln.description}</p>
                                <p>危险等级: ${vuln.severity}</p>
                                <p>状态: ${vuln.status}</p>
                            </div>
                        `);
                    });
                },
                complete: function() {
                    hideLoading();
                    $('#scanButton').prop('disabled', false);
                }
            });
        }, 1500); // 模拟加载时间
    });

    // 漏洞验证功能
    $('.verify-btn').click(function() {
        const vulnId = $(this).data('id');
        showLoading();

        setTimeout(function() {
            $.ajax({
                url: `/api/verify/${vulnId}`,
                method: 'POST',
                success: function(response) {
                    alert(response.message);
                },
                complete: function() {
                    hideLoading();
                }
            });
        }, 2000); // 模拟验证时间
    });

    // 漏洞利用功能
    $('.exploit-btn').click(function() {
        const vulnId = $(this).data('id');
        showLoading();

        setTimeout(function() {
            $.ajax({
                url: `/api/exploit/${vulnId}`,
                method: 'POST',
                success: function(response) {
                    alert(response.message);
                },
                complete: function() {
                    hideLoading();
                }
            });
        }, 2500); // 模拟利用时间
    });

    // 漏洞修复功能
    $('.fix-btn').click(function() {
        const vulnId = $(this).data('id');
        showLoading();

        setTimeout(function() {
            $.ajax({
                url: `/api/fix/${vulnId}`,
                method: 'POST',
                success: function(response) {
                    alert(response.message);
                },
                complete: function() {
                    hideLoading();
                }
            });
        }, 3000); // 模拟修复时间
    });

    // 报告生成功能
    $('#generateReport').click(function() {
        const reportType = $('#reportType').val();
        showLoading();

        setTimeout(function() {
            $('#reportContent').show();
            $('.report-section').html(`
                <div class="alert alert-success">
                    <h4>报告生成完成</h4>
                    <p>报告类型: ${reportType}</p>
                    <p>生成时间: ${new Date().toLocaleString()}</p>
                    <p>发现漏洞总数: ${Math.floor(Math.random() * 10) + 1}个</p>
                    <hr>
                    <h5>漏洞统计</h5>
                    <ul>
                        <li>高危漏洞: ${Math.floor(Math.random() * 5)}个</li>
                        <li>中危漏洞: ${Math.floor(Math.random() * 5)}个</li>
                        <li>低危漏洞: ${Math.floor(Math.random() * 5)}个</li>
                    </ul>
                </div>
            `);
            hideLoading();
        }, 2000); // 模拟报告生成时间
    });

    // 为所有按钮添加点击效果
    $('.btn').click(function() {
        $(this).addClass('active');
        setTimeout(() => {
            $(this).removeClass('active');
        }, 200);
    });

    // 加载验证结果列表
    function loadVerifyResults() {
        showLoading();
        setTimeout(function() {
            $.ajax({
                url: '/api/verify/list',
                method: 'GET',
                success: function(response) {
                    const tbody = $('#verifyTable tbody');
                    tbody.empty();
                    response.forEach(function(result) {
                        tbody.append(`
                            <tr>
                                <td>${result.vuln_id}</td>
                                <td>${result.verify_time}</td>
                                <td><span class="badge bg-${result.verify_result === '已确认' ? 'success' : 'warning'}">${result.verify_result}</span></td>
                                <td>${result.verify_method}</td>
                                <td>${result.confidence}</td>
                                <td>
                                    <button class="btn btn-sm btn-info" onclick="showVerifyDetails('${result.verify_details}')">查看详情</button>
                                </td>
                            </tr>
                        `);
                    });
                },
                complete: function() {
                    hideLoading();
                }
            });
        }, 1500);
    }

    // 加载报告列表
    function loadReports() {
        showLoading();
        setTimeout(function() {
            $.ajax({
                url: '/api/reports/list',
                method: 'GET',
                success: function(response) {
                    const tbody = $('#reportsTable tbody');
                    tbody.empty();
                    response.forEach(function(report) {
                        tbody.append(`
                            <tr>
                                <td>${report.report_time}</td>
                                <td>${report.report_type}</td>
                                <td>${report.target_ip}</td>
                                <td>${report.total_vulns}</td>
                                <td>
                                    <span class="badge bg-danger">高危: ${report.high_risk}</span>
                                    <span class="badge bg-warning">中危: ${report.medium_risk}</span>
                                    <span class="badge bg-info">低危: ${report.low_risk}</span>
                                </td>
                                <td><span class="badge bg-${report.status === '已生成' ? 'success' : 'primary'}">${report.status}</span></td>
                                <td>
                                    <button class="btn btn-sm btn-primary">下载报告</button>
                                </td>
                            </tr>
                        `);
                    });
                },
                complete: function() {
                    hideLoading();
                }
            });
        }, 1500);
    }

// 加载历史记录
$(document).ready(function() {
    loadHistory();  // 页面加载时自动加载历史记录
});

function loadHistory() {
    $.ajax({
        url: '/api/history/list',
        method: 'GET',
        success: function(records) {
            const tbody = $('#historyTableBody');
            tbody.empty();  // 清空旧数据

            records.forEach(record => {
                // 根据状态渲染不同徽章样式
                const statusClass = `status-${record.status}`;
                const statusBadge = `<span class="status-badge ${statusClass}">${record.status}</span>`;

                // 漏洞数显示（失败时显示0）
                const vulnCount = record.status === 'failed' ? 0 : record.vulnerabilities_found;

                // 动态插入表格行
                tbody.append(`
                    <tr>
                        <td>${record.timestamp}</td>
                        <td>${record.target_ip}</td>
                        <td>${record.scan_type}</td>
                        <td>${vulnCount}</td>
                        <td>${statusBadge}</td>
                        <td>${record.scan_duration || 'N/A'}</td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary" 
                                    onclick="showDetails('${record.scan_id}')">
                                查看详情
                            </button>
                        </td>
                    </tr>
                `);
            });
        },
        error: function(xhr) {
            alert(`加载历史记录失败: ${xhr.responseText}`);
        }
    });
}

function showDetails(scanId) {
    // 调用详情接口获取漏洞详情（需后端实现 /api/history/detail）
    $.ajax({
        url: `/api/history/detail/${scanId}`,
        method: 'GET',
        success: function(details) {
            // 使用 Bootstrap 模态框显示详情
            const modalHtml = `
                <div class="modal fade" id="detailsModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">扫描详情（${scanId}）</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <h6>目标IP: ${details.target_ip}</h6>
                                <h6>扫描类型: ${details.scan_type}</h6>
                                <h6>扫描时长: ${details.scan_duration || 'N/A'}</h6>
                                ${details.status === 'failed' ? 
                                    `<div class="alert alert-danger">错误信息: ${details.error_message}</div>` :
                                    `<h6>发现漏洞（共${details.vulnerabilities_found}个）:</h6>
                                     <ul>${details.vuln_details.map(v => 
                                         `<li>${v.type}（${v.severity}）: ${v.id}</li>`
                                     ).join('')}</ul>`
                                }
                            </div>
                        </div>
                    </div>
                </div>
            `;
            $('body').append(modalHtml);
            new bootstrap.Modal('#detailsModal').show();
        }
    });
}

    // 显示验证详情
    function showVerifyDetails(details) {
        alert(details);
    }

    // 显示历史记录详情
    function showHistoryDetails(details) {
        alert(`高危漏洞: ${details.high_risk}个\n中危漏洞: ${details.medium_risk}个\n低危漏洞: ${details.low_risk}个`);
    }

    // 根据当前页面自动加载相应的数据
    if (window.location.pathname === '/verify') {
        loadVerifyResults();
    } else if (window.location.pathname === '/report') {
        loadReports();
    } else if (window.location.pathname === '/history') {
        loadHistory();
    }
});
