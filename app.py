import json
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import random
import sqlite3
import time
from backend.history_manager import HistoryManager
from backend.scanners.nmap_scanner import NmapScanner
from config.config import *
import logging

app = Flask(__name__)
# 初始化 HistoryManager
history_manager = HistoryManager()
# 初始化 NmapScanner
scanner = NmapScanner(SCAN_CONFIG)

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
    history = history_manager.get_history()  # 调用方法
    return render_template('history.html', history=history)


@app.route('/api/scan', methods=['POST'])
def start_scan():
    data = request.json
    target = data.get('target')
    scan_type = data.get('scan_type', 'quick')
    scan_id = f"SCAN_{int(time.time())}"  # 生成唯一扫描ID（时间戳+随机数）

    history_manager = HistoryManager()
    try:
        # 1. 扫描开始时记录「处理中」状态
        history_manager.add_record({
            "scan_id": scan_id,
            "target_ip": target,
            "scan_type": scan_type,
            "status": "pending",
            "vulnerabilities_found": 0,  # 初始为0，扫描完成后更新
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # 2. 模拟真实扫描过程（耗时2-5秒）
        start_time = datetime.now()
        time.sleep(random.randint(2, 5))  # 替换为实际扫描逻辑

        # 3. 扫描完成后生成结果
        end_time = datetime.now()
        scan_duration = f"{(end_time - start_time).seconds}秒"
        found_vulns = [  # 模拟漏洞数据（实际从扫描器获取）
            {"id": f"VULN-{i}", "type": "SQL注入", "severity": "高危"}
            for i in range(random.randint(1, 5))
        ]

        # 4. 更新历史记录为「完成」状态
        history_manager.update_record(scan_id, {
            "status": "completed",
            "vulnerabilities_found": len(found_vulns),
            "scan_duration": scan_duration,
            "vuln_details": json.dumps(found_vulns),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 更新为完成时间
        })

        return jsonify({
            "status": "success",
            "scan_id": scan_id,
            "results": {"vulns": found_vulns, "duration": scan_duration}
        })

    except Exception as e:
        # 扫描失败时记录错误信息
        history_manager.update_record(scan_id, {
            "status": "failed",
            "error_message": str(e)
        })
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/scan/record', methods=['POST'])
def record_scan_result():
    data = request.json
    scan_id = f"SCAN_{int(datetime.now().timestamp())}"
    data["scan_id"] = scan_id
    history_manager.add_record(data)
    return jsonify({"message": "扫描记录保存成功", "scan_id": scan_id})

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


# app.py（添加历史记录列表接口）
@app.route('/api/history/list', methods=['GET'])
def get_history_list():
    # 从请求参数中获取分页信息（默认page=1，每页10条）
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page  # 计算偏移量

    # 调用 HistoryManager 的 get_history 方法
    history_manager = HistoryManager()
    records = history_manager.get_history(limit=per_page, offset=offset)

    # 转换为前端需要的格式（可选）
    formatted_records = [{
        "scan_id": rec["scan_id"],
        "timestamp": rec["timestamp"],
        "target_ip": rec["target_ip"],
        "scan_type": rec["scan_type"],
        "vulnerabilities_found": rec["vulnerabilities_found"],
        "status": rec["status"],
        "scan_duration": rec.get("scan_duration", "N/A")
    } for rec in records]

    return jsonify({
        "total": len(records),  # 实际项目中建议查询总记录数
        "page": page,
        "per_page": per_page,
        "data": formatted_records
    })
def get_history():
    try:
        # 从 URL 参数获取分页信息
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        offset = (page - 1) * per_page

        # 添加日志，确认参数
        app.logger.info(f"获取历史记录: page={page}, per_page={per_page}, offset={offset}")

        records = history_manager.get_history(limit=per_page, offset=offset)

        # 添加日志，确认查询结果
        app.logger.info(f"成功获取 {len(records)} 条历史记录")

        return jsonify(records)
    except Exception as e:
        # 记录详细的错误信息
        app.logger.error(f'获取历史记录失败: {str(e)}', exc_info=True)
        return jsonify({
            'error': '获取历史记录失败',
            'details': str(e)
        }), 500
@app.route('/test/add_record', methods=['GET'])
def test_add_record():
    test_data = {
        "scan_id": "TEST-1234",
        "target": "127.0.0.1",
        "scan_type": "测试扫描",
        "found_vulnerabilities": [{"id": "TEST-001", "name": "测试漏洞"}]
    }

    history_manager.add_record(test_data)
    return "测试记录已添加"


# 保存扫描记录接口（与前端fetch匹配）
@app.route('/api/scan/save', methods=['POST'])
def save_scan_record():
    scan_data = request.get_json()
    history_manager.add_record(scan_data)
    return jsonify({"status": "success"})



if __name__ == '__main__':
    app.run(debug=True)

