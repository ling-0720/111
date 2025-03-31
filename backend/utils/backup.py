import os
import shutil
import tarfile
from datetime import datetime
from typing import Dict, Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def create_backup(target_info: Dict) -> str:
    """
    创建目标系统的配置备份
    
    Args:
        target_info: 目标系统信息
        
    Returns:
        str: 备份ID
    """
    try:
        # 生成备份ID
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 创建备份目录
        backup_dir = os.path.join('backups', backup_id)
        os.makedirs(backup_dir, exist_ok=True)
        
        # 记录目标信息
        with open(os.path.join(backup_dir, 'target_info.txt'), 'w') as f:
            for key, value in target_info.items():
                f.write(f"{key}: {value}\n")
        
        logger.info(f"Created backup {backup_id} for {target_info.get('host', 'unknown')}")
        return backup_id
        
    except Exception as e:
        logger.error(f"Failed to create backup: {str(e)}")
        raise
        
def restore_backup(backup_id: str) -> bool:
    """
    从备份恢复系统配置
    
    Args:
        backup_id: 备份ID
        
    Returns:
        bool: 是否成功恢复
    """
    try:
        backup_dir = os.path.join('backups', backup_id)
        if not os.path.exists(backup_dir):
            raise FileNotFoundError(f"Backup {backup_id} not found")
            
        # 读取目标信息
        target_info = {}
        with open(os.path.join(backup_dir, 'target_info.txt'), 'r') as f:
            for line in f:
                key, value = line.strip().split(': ', 1)
                target_info[key] = value
                
        logger.info(f"Restored backup {backup_id} for {target_info.get('host', 'unknown')}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to restore backup: {str(e)}")
        return False
        
def list_backups() -> list:
    """
    列出所有可用的备份
    
    Returns:
        list: 备份列表
    """
    try:
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            return []
            
        backups = []
        for item in os.listdir(backup_dir):
            if os.path.isdir(os.path.join(backup_dir, item)) and item.startswith('backup_'):
                backups.append(item)
                
        return sorted(backups, reverse=True)
        
    except Exception as e:
        logger.error(f"Failed to list backups: {str(e)}")
        return []
        
def delete_backup(backup_id: str) -> bool:
    """
    删除指定的备份
    
    Args:
        backup_id: 备份ID
        
    Returns:
        bool: 是否成功删除
    """
    try:
        backup_dir = os.path.join('backups', backup_id)
        if not os.path.exists(backup_dir):
            return False
            
        shutil.rmtree(backup_dir)
        logger.info(f"Deleted backup {backup_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to delete backup: {str(e)}")
        return False 