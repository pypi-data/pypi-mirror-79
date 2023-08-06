from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager


class Runner:
    def __init__(self, inventory_files, playbook_file, **context_cli_args):
        """
        Args:
            inverntory_files (list): list of file paths to inventory files
            playbook_file (list): list of paths to playbook files
        """

        loader = DataLoader()
        context.CLIARGS = ImmutableDict(
            become=context_cli_args.get('become', False),
            become_method=context_cli_args.get('become_method', 'sudo'),
            become_user=context_cli_args.get('become_user', 'root'),
            check=context_cli_args.get('check', False),
            connection=context_cli_args.get('connection', 'ssh'),
            forks=context_cli_args.get('forks', 100),
            listhosts=context_cli_args.get('listhosts', False),
            listtags=context_cli_args.get('listtags', False),
            listtasks=context_cli_args.get('listtasks', False),
            module_path=context_cli_args.get('module_path', None),
            private_key_file=context_cli_args.get('private_key_file', None),
            remote_user=context_cli_args.get('remote_user', 'root'),
            scp_extra_args=context_cli_args.get('scp_extra_args', None),
            sftp_extra_args=context_cli_args.get('sftp_extra_args', None),
            ssh_common_args=context_cli_args.get('ssh_common_args', None),
            ssh_extra_args=context_cli_args.get('ssh_extra_args', None),
            start_at_task=context_cli_args.get('start_at_task', None),
            syntax=context_cli_args.get('syntax', False),
            tags=context_cli_args.get('tags', {}),
            verbosity=context_cli_args.get('verbosity', True),
        )

        inventory = InventoryManager(loader=loader, sources=(inventory_files))
        variable_manager = VariableManager(
            loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))
        self.pbex = PlaybookExecutor(
            playbooks=[playbook_file], inventory=inventory, variable_manager=variable_manager, loader=loader,
            passwords={})

    def run(self):
        return self.pbex.run()
