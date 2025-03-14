from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import random
import time
# from backend.scanners.nmap_scanner import NmapScanner
# from backend.verifiers.metasploit_verifier import MetasploitVerifier
# from backend.exploiters.metasploit_exploiter import MetasploitExploiter
# from backend.fixers.auto_fixer import AutoFixer
# from backend.config import SCAN_CONFIG, METASPLOIT_CONFIG
from config.config import *

app = Flask(__name__)

# 注释掉扫描器初始化
# scanner = NmapScanner(SCAN_CONFIG)
# verifier = MetasploitVerifier(METASPLOIT_CONFIG)
# exploiter = MetasploitExploiter(METASPLOIT_CONFIG)
# fixer = AutoFixer()

# 模拟的漏洞数据
mock_vulnerabilities = [
    {
        "id": 1,
        "name": "CVE-2023-1234",
        "description": "IoT设备远程代码执行漏洞",
        "severity": "高危",
        "status": "未修复",
        "affected_device": "智能摄像头",
        "discovery_date": "2024-03-15"
    },
    {
        "id": 2,
        "name": "CVE-2023-5678",
        "description": "智能摄像头认证绕过漏洞",
        "severity": "中危",
        "status": "已修复",
        "affected_device": "智能门锁",
        "discovery_date": "2024-03-16"
    },
    {
        "id": 3,
        "name": "CVE-2024-9012",
        "description": "智能家居控制器后门漏洞",
        "severity": "高危",
        "status": "修复中",
        "affected_device": "智能家居控制器",
        "discovery_date": "2024-03-17"
    },
    {
        "id": 4,
        "name": "CVE-2024-3456",
        "description": "智能音箱固件升级漏洞",
        "severity": "低危",
        "status": "已修复",
        "affected_device": "智能音箱",
        "discovery_date": "2024-03-18"
    },
    {
        "id": 5,
        "name": "CVE-2024-7890",
        "description": "智能冰箱网络通信漏洞",
        "severity": "中危",
        "status": "未修复",
        "affected_device": "智能冰箱",
        "discovery_date": "2024-03-19"
    },
    {
        "id": 6,
        "name": "CVE-2024-1111",
        "description": "智能门铃固件漏洞",
        "severity": "高危",
        "status": "未修复",
        "affected_device": "智能门铃",
        "discovery_date": "2024-03-20"
    },
    {
        "id": 7,
        "name": "CVE-2024-2222",
        "description": "智能手环数据泄露漏洞",
        "severity": "中危",
        "status": "已修复",
        "affected_device": "智能手环",
        "discovery_date": "2024-03-21"
    },
    {
        "id": 8,
        "name": "CVE-2024-3333",
        "description": "智能电视后门程序",
        "severity": "高危",
        "status": "修复中",
        "affected_device": "智能电视",
        "discovery_date": "2024-03-22"
    },
    {
        "id": 9,
        "name": "CVE-2024-4444",
        "description": "智能空调远程控制漏洞",
        "severity": "中危",
        "status": "未修复",
        "affected_device": "智能空调",
        "discovery_date": "2024-03-23"
    },
    {
        "id": 10,
        "name": "CVE-2024-5555",
        "description": "智能插座越权访问漏洞",
        "severity": "低危",
        "status": "已修复",
        "affected_device": "智能插座",
        "discovery_date": "2024-03-24"
    },
    {
        "id": 11,
        "name": "CVE-2024-6666",
        "description": "智能窗帘控制器漏洞",
        "severity": "中危",
        "status": "未修复",
        "affected_device": "智能窗帘",
        "discovery_date": "2024-03-25"
    },
    {
        "id": 12,
        "name": "CVE-2024-7777",
        "description": "智能门锁蓝牙协议漏洞",
        "severity": "高危",
        "status": "修复中",
        "affected_device": "智能门锁",
        "discovery_date": "2024-03-26"
    },
    {
        "id": 13,
        "name": "CVE-2024-8888",
        "description": "智能手表GPS定位漏洞",
        "severity": "中危",
        "status": "已修复",
        "affected_device": "智能手表",
        "discovery_date": "2024-03-27"
    },
    {
        "id": 14,
        "name": "CVE-2024-9999",
        "description": "智能体重秤数据篡改漏洞",
        "severity": "低危",
        "status": "未修复",
        "affected_device": "智能体重秤",
        "discovery_date": "2024-03-28"
    },
    {
        "id": 15,
        "name": "CVE-2024-1010",
        "description": "智能烤箱远程控制漏洞",
        "severity": "高危",
        "status": "未修复",
        "affected_device": "智能烤箱",
        "discovery_date": "2024-03-29"
    },
    {
        "id": 16,
        "name": "CVE-2024-1212",
        "description": "智能洗衣机固件漏洞",
        "severity": "中危",
        "status": "修复中",
        "affected_device": "智能洗衣机",
        "discovery_date": "2024-03-30"
    },
    {
        "id": 17,
        "name": "CVE-2024-1313",
        "description": "智能垃圾桶越权访问",
        "severity": "低危",
        "status": "已修复",
        "affected_device": "智能垃圾桶",
        "discovery_date": "2024-03-31"
    },
    {
        "id": 18,
        "name": "CVE-2024-1414",
        "description": "智能床垫数据泄露漏洞",
        "severity": "中危",
        "status": "未修复",
        "affected_device": "智能床垫",
        "discovery_date": "2024-04-01"
    },
    {
        "id": 19,
        "name": "CVE-2024-1515",
        "description": "智能浴室镜远程控制漏洞",
        "severity": "高危",
        "status": "修复中",
        "affected_device": "智能浴室镜",
        "discovery_date": "2024-04-02"
    },
    {
        "id": 20,
        "name": "CVE-2024-1616",
        "description": "智能晾衣架认证绕过漏洞",
        "severity": "中危",
        "status": "未修复",
        "affected_device": "智能晾衣架",
        "discovery_date": "2024-04-03"
    }
]

# 模拟的历史记录数据
mock_history = [
    {
        "id": 1,
        "scan_time": "2024-03-20 10:30",
        "target": "192.168.1.100",
        "vulnerabilities_found": 3,
        "status": "已完成",
        "scan_type": "完整扫描",
        "duration": "5分钟"
    },
    {
        "id": 2,
        "scan_time": "2024-03-19 15:45",
        "target": "192.168.1.200",
        "vulnerabilities_found": 2,
        "status": "已完成",
        "scan_type": "快速扫描",
        "duration": "2分钟"
    },
    {
        "id": 3,
        "scan_time": "2024-03-18 09:15",
        "target": "192.168.1.150",
        "vulnerabilities_found": 5,
        "status": "已完成",
        "scan_type": "漏洞扫描",
        "duration": "8分钟"
    },
    {
        "id": 4,
        "scan_time": "2024-03-17 14:20",
        "target": "192.168.1.300",
        "vulnerabilities_found": 1,
        "status": "已完成",
        "scan_type": "快速扫描",
        "duration": "3分钟"
    },
    {
        "id": 5,
        "scan_time": "2024-03-16 11:30",
        "target": "192.168.1.120",
        "vulnerabilities_found": 4,
        "status": "已完成",
        "scan_type": "完整扫描",
        "duration": "6分钟"
    },
    {
        "id": 6,
        "scan_time": "2024-03-15 13:45",
        "target": "192.168.1.130",
        "vulnerabilities_found": 2,
        "status": "已完成",
        "scan_type": "快速扫描",
        "duration": "3分钟"
    },
    {
        "id": 20,
        "scan_time": "2024-03-01 16:20",
        "target": "192.168.1.250",
        "vulnerabilities_found": 3,
        "status": "已完成",
        "scan_type": "漏洞扫描",
        "duration": "7分钟"
    }
]

# 模拟的修复建议数据
mock_fixes = [
    {
        "id": 1,
        "vulnerability_id": "CVE-2023-1234",
        "fix_description": "更新设备固件至最新版本v2.1.5",
        "steps": [
            "登录设备管理界面",
            "进入系统更新选项",
            "下载并安装最新固件",
            "重启设备完成更新"
        ],
        "estimated_time": "30分钟"
    },
    {
        "id": 2,
        "vulnerability_id": "CVE-2023-5678",
        "fix_description": "修改默认密码并启用双因素认证",
        "steps": [
            "访问设备配置页面",
            "修改管理员密码",
            "启用双因素认证",
            "配置认证应用"
        ],
        "estimated_time": "15分钟"
    },
    {
        "id": 3,
        "vulnerability_id": "CVE-2024-9012",
        "fix_description": "关闭不必要的系统服务并更新安全补丁",
        "steps": [
            "检查系统服务列表",
            "关闭非必要服务",
            "安装最新安全补丁",
            "重启系统完成更新"
        ],
        "estimated_time": "45分钟"
    },
    {
        "id": 20,
        "vulnerability_id": "CVE-2024-1616",
        "fix_description": "升级认证模块并加强访问控制",
        "steps": [
            "更新认证模块",
            "配置访问控制策略",
            "测试新认证机制",
            "部署更新"
        ],
        "estimated_time": "25分钟"
    }
]

# 模拟的漏洞验证结果数据
mock_verify_results = [
    {
        "id": 1,
        "vuln_id": "CVE-2023-1234",
        "verify_time": "2024-03-20 10:30",
        "verify_result": "已确认",
        "verify_method": "Metasploit模块验证",
        "verify_details": "使用CVE-2023-1234验证模块成功复现漏洞",
        "confidence": "95%"
    },
    # ... 继续添加更多验证结果 ...
]

# 模拟的报告数据
mock_reports = [
    {
        "id": 1,
        "report_time": "2024-03-20 11:30",
        "report_type": "完整报告",
        "target_ip": "192.168.1.100",
        "total_vulns": 5,
        "high_risk": 2,
        "medium_risk": 2,
        "low_risk": 1,
        "status": "已生成"
    },
    # ... 继续添加更多报告 ...
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/verify')
def verify():
    return render_template('verify.html', vulnerabilities=mock_vulnerabilities)

@app.route('/exploit')
def exploit():
    return render_template('exploit.html', vulnerabilities=mock_vulnerabilities)

@app.route('/fix')
def fix():
    return render_template('fix.html', vulnerabilities=mock_vulnerabilities, fixes=mock_fixes)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/history')
def history():
    return render_template('history.html', history=mock_history)

@app.route('/api/scan', methods=['POST'])
def start_scan():
    """启动漏洞扫描"""
    data = request.json
    target = data.get('target')
    scan_type = data.get('scan_type', 'quick')
    
    # 返回模拟的扫描结果
    mock_result = {
        'scan_id': f"SCAN_{int(time.time())}",
        'target': target,
        'scan_type': scan_type,
        'start_time': datetime.now().isoformat(),
        'status': 'completed',
        'results': {
            'hosts_scanned': 1,
            'vulnerabilities_found': random.randint(1, 5),
            'scan_duration': f"{random.randint(10, 60)}s"
        }
    }
    return jsonify(mock_result)

@app.route('/api/verify/<vuln_id>', methods=['POST'])
def verify_vulnerability(vuln_id):
    """验证漏洞"""
    data = request.json
    try:
        result = verifier.verify(data['vulnerability'], data['target_info'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exploit/<vuln_id>', methods=['POST'])
def exploit_vulnerability(vuln_id):
    """利用漏洞"""
    data = request.json
    try:
        result = exploiter.exploit(data['vulnerability'], data['target_info'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fix/<vuln_id>', methods=['POST'])
def fix_vulnerability(vuln_id):
    """修复漏洞"""
    data = request.json
    try:
        result = fixer.fix(data['vulnerability'], data['target_info'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify/list', methods=['GET'])
def get_verify_results():
    # 生成10条验证结果数据
    results = []
    for i in range(10):
        result = {
            "id": i + 1,
            "vuln_id": f"CVE-2024-{1000 + i}",
            "verify_time": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M"),
            "verify_result": random.choice(["已确认", "未确认", "验证失败"]),
            "verify_method": random.choice(["Metasploit模块验证", "手动验证", "自动化脚本验证"]),
            "verify_details": f"漏洞{i+1}验证详细信息...",
            "confidence": f"{random.randint(70, 99)}%"
        }
        results.append(result)
    return jsonify(results)

@app.route('/api/reports/list', methods=['GET'])
def get_reports():
    # 生成10条报告数据
    reports = []
    for i in range(10):
        high_risk = random.randint(0, 5)
        medium_risk = random.randint(1, 6)
        low_risk = random.randint(1, 4)
        report = {
            "id": i + 1,
            "report_time": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M"),
            "report_type": random.choice(["完整报告", "摘要报告", "技术报告"]),
            "target_ip": f"192.168.1.{random.randint(100, 200)}",
            "total_vulns": high_risk + medium_risk + low_risk,
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk,
            "status": random.choice(["已生成", "生成中", "已归档"])
        }
        reports.append(report)
    return jsonify(reports)

@app.route('/api/history/list', methods=['GET'])
def get_history():
    # 生成10条历史记录数据
    history = []
    for i in range(10):
        record = {
            "id": i + 1,
            "scan_time": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M"),
            "target": f"192.168.1.{random.randint(100, 200)}",
            "vulnerabilities_found": random.randint(1, 8),
            "status": random.choice(["已完成", "扫描中", "已中止"]),
            "scan_type": random.choice(["完整扫描", "快速扫描", "漏洞扫描"]),
            "duration": f"{random.randint(2, 10)}分钟",
            "details": {
                "high_risk": random.randint(0, 3),
                "medium_risk": random.randint(1, 4),
                "low_risk": random.randint(0, 2)
            }
        }
        history.append(record)
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 