import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('container', ['moleculemysql-database-mysql', 'moleculemysql-database-mysql-backup', 'moleculepsql-database-postgres', 'moleculepsql-database-postgres-backup'])
def test_docker_db_containers(host, container):
    command = host.run("docker ps")
    assert (container) in command.stdout


def test_docker_db_mysql_backup(host):
    command = host.run('docker exec -i moleculemysql-database-mysql-backup /usr/local/bin/automysqlbackup')
    assert "/backup/daily/molecule/molecule_" in command.stdout


def test_docker_db_postgresql_backup(host):
    command = host.run('docker exec -i moleculepsql-database-postgres-backup /usr/sbin/autopostgresqlbackup')
    assert "/backups/daily/molecule/molecule_" in command.stdout
