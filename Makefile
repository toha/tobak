build:

readme:
	@markdown README.md > README.html

install:
	mkdir -p /var/lib/tobak
	mkdir -p /usr/share/tobak
	mkdir -p /etc/tobak
	cp cfg/profiles.json.example /etc/tobak/profiles.json
	cp cfg/tobak.json.example /etc/tobak/tobak.json
	cp -r py/* /usr/share/tobak
	ln -s /usr/share/tobak/tobak.py /usr/bin/tobak
	chmod +x /usr/share/tobak/tobak.py
	chmod +x /usr/bin/tobak

update:
	rm -rf /usr/share/tobak
	mkdir -p /usr/share/tobak
	cp -r py/* /usr/share/tobak
	chmod +x /usr/share/tobak/tobak.py
	chmod +x /usr/bin/tobak	

.PHONY: build