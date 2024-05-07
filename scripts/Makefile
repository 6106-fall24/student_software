.PHONY: upload-github-aws 
upload-github-aws:
	aws s3 cp github.py s3://6172-fall20-public/github.py

locker_software_public_path="/mit/6.172/public/software"
locker_arch_bin_path="/mit/6.172/arch/amd64_ubuntu1804/bin"

upload-github-athena:
	cp github.py ${locker_software_public_path}/github.py
	ln -s ${locker_software_public_path}/github.py ${locker_arch_bin_path}/github-setup-6106

upload-run-vscode-athena:
	cp run-vscode.sh ${locker_software_public_path}/run-vscode.sh
	ln -s ${locker_software_public_path}/run-vscode.sh ${locker_arch_bin_path}/run-vscode-6106
