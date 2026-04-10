# Můj Kaktus pro Home Assistant

HACS integrace pro sledování stavu kreditu a historie volání, SMS, dat a dobíjení v síti Kaktus.

## Vlastnosti
- Sledování aktuálního stavu kreditu.
- Historie volání (poslední záznamy v atributech).
- Historie SMS (poslední záznamy v atributech).
- Historie dat (poslední záznamy v atributech).
- Historie dobíjení (poslední záznamy v atributech).

## Instalace

### Přes HACS (Doporučeno)
1. Otevřete HACS ve svém Home Assistantovi.
2. Jděte do sekce **Integrations**.
3. Klikněte na tři tečky v pravém horním rohu a vyberte **Custom repositories**.
4. Vložte URL tohoto repozitáře: `https://github.com/pvranik/hacs_mujkaktus` a vyberte kategorii **Integration**.
5. Klikněte na **Add** a poté integraci nainstalujte.
6. Restartujte Home Assistanta.

### Manuálně
1. Stáhněte si tento repozitář.
2. Zkopírujte složku `custom_components/mujkaktus` do vaší složky `config/custom_components/`.
3. Restartujte Home Assistanta.

## Nastavení
1. V Home Assistantovi jděte do **Settings** -> **Devices & Services**.
2. Klikněte na **Add Integration**.
3. Vyhledejte **Můj Kaktus**.
4. Zadejte své přihlašovací jméno a heslo k samoobsluze Kaktus.

## Poděkování
Tato integrace využívá knihovnu [pymujkaktus](https://github.com/pvranik/pymujkaktus).