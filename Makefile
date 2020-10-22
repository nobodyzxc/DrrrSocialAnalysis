KEY=meta/key.txt
LOUNGE=lounge
CUR_FN=lounge-2020-10-22
CUR_BIN=meta/$(CUR_FN).bin
CUR_ZIP=download/$(CUR_FN).zip

EXECUTABLES = openssl unzip xargs
K := $(foreach exec,$(EXECUTABLES),\
        $(if $(shell which $(exec) 2>/dev/null),some string,$(error "Please install $(exec)")))

data: | $(CUR_ZIP)
	@unzip $(CUR_ZIP) -d $(LOUNGE)

key:
	openssl genrsa -aes128 -passout stdin -out $(KEY) 4096

encrypt:
	@echo -ne "Input string to encrypt:"; read s; echo $$s | openssl rsautl -inkey $(KEY) -encrypt > encrypted.bin

decrypt:
	@echo -ne "Input file:"; read fn; openssl rsautl -inkey $(KEY) -decrypt < $$fn

$(CUR_ZIP):
	@openssl rsautl -inkey $(KEY) -decrypt < $(CUR_BIN) | xargs -i ./fdrive.sh "{} $(CUR_ZIP)"

clean:
	rm -rf $(CUR_ZIP) $(LOUNGE)/*.json
