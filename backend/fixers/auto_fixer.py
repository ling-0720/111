import time
from typing import Dict, List, Optional
import paramiko
from ..core.base_fixer import BaseFixer, FixException
from ..models.vulnerability import Vulnerability, VulnerabilityStatus
from ..utils.network import resolve_host
from ..utils.backup import create_backup, restore_backup

    def _create_fix_plan(self, vulnerability: Vulnerability, target_info: Dict) -> Dict:
        """创建修复方案"""
        # 根据漏洞类型选择修复模板
        template = self._select_fix_template(vulnerability)
        if not template:
            return None
            
        return {
            'steps': self._customize_fix_steps(template, vulnerability, target_info),
            'verification': template['verification_steps'],
            'rollback': template['rollback_steps']
        }
    
    def _execute_fix_plan(self, fix_plan: Dict, target_info: Dict) -> Dict:
        """执行修复方案"""
        try:
            # 建立SSH连接
            ssh = self._create_ssh_connection(target_info)
            
            results = []
            # 执行每个修复步骤
            for step in fix_plan['steps']:
                step_result = self._execute_fix_step(ssh, step)
                results.append(step_result)
                
                if not step_result['success']:
                    # 如果步骤失败，中断修复
                    return {
                        'status': 'failed',
                        'step_results': results,
                        'failed_step': step['name']
                    }
            
            return {
                'status': 'success',
                'step_results': results
            }
            
        finally:
            if ssh:
                ssh.close()
    
    def _execute_fix_step(self, ssh: paramiko.SSHClient, step: Dict) -> Dict:
        """执行单个修复步骤"""
        try:
            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(step['command'])
            exit_code = stdout.channel.recv_exit_status()
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            success = exit_code == 0 and self._verify_step_output(output, step)
            
            return {
                'step': step['name'],
                'success': success,
                'output': output,
                'error': error,
                'exit_code': exit_code
            }
            
        except Exception as e:
            return {
                'step': step['name'],
                'success': False,
                'error': str(e)
            }
    
    def verify_fix(self, vulnerability: Vulnerability, fix_id: str) -> Dict:
        """验证修复结果"""
        if fix_id not in self.running_fixes:
            return {'status': 'not_found'}
            
        fix_info = self.running_fixes[fix_id]
        
        try:
            # 执行验证步骤
            verification_result = self._execute_verification(
                fix_info['fix_plan']['verification'],
                fix_info['target_info']
            )
            
            return {
                'status': 'success' if verification_result['verified'] else 'failed',
                'details': verification_result
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def rollback(self, fix_id: str) -> bool:
        """回滚修复操作"""
        if fix_id not in self.running_fixes:
            return False
            
        fix_info = self.running_fixes[fix_id]
        
        try:
            # 恢复备份
            restore_backup(fix_info['backup_id'])
            
            # 执行回滚步骤
            for step in reversed(fix_info['fix_plan']['rollback']):
                self._execute_rollback_step(step, fix_info['target_info'])
            
            return True
            
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            return False
    
    def get_fix_status(self, fix_id: str) -> Dict:
        """获取修复任务状态"""
        if fix_id not in self.running_fixes:
            return {'status': 'not_found'}
        
        fix_info = self.running_fixes[fix_id]
        
        return {
            'status': fix_info['status'],
            'start_time': fix_info['start_time'].isoformat(),
            'vulnerability': fix_info['vulnerability'].to_dict(),
            'last_update': datetime.now().isoformat()
        }
    
    def _load_fix_templates(self) -> Dict:
        """加载修复模板"""
        # 实际实现中应该从配置文件或数据库加载
        return {
            'sql_injection': {
                'name': 'SQL注入修复',
                'steps': [
                    {
                        'name': '更新Web应用',
                        'command': 'apt-get update && apt-get upgrade -y'
                    },
                    {
                        'name': '配置SQL过滤',
                        'command': 'sed -i "s/filter_sql=0/filter_sql=1/" /etc/webapp/config.ini'
                    }
                ],
                'verification_steps': [
                    'check_sql_filter_config',
                    'test_sql_injection'
                ],
                'rollback_steps': [
                    'restore_original_config',
                    'restart_services'
                ]
            },
            # 更多模板...
        }
    
    def _create_ssh_connection(self, target_info: Dict) -> paramiko.SSHClient:
        """创建SSH连接"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(
                target_info['host'],
                username=target_info.get('username'),
                password=target_info.get('password'),
                key_filename=target_info.get('key_file')
            )
            return ssh
        except Exception as e:
            raise FixException(f"Failed to establish SSH connection: {str(e)}") 