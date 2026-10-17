"""Generate a compatibility overlay from locally supplied Minecraft assets."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path


def select_one(folder, pattern):
    matches = sorted(p for p in folder.glob(pattern)
                     if p.name != 'Lazarus - Apocalypse Reanimated Compat.zip')
    if len(matches) != 1:
        raise ValueError(f'Esperado um arquivo {pattern} em {folder}; encontrados {len(matches)}. Informe o arquivo explicitamente.')
    return matches[0]


def build(apocalypse, reanimated, output):
    with zipfile.ZipFile(apocalypse) as mod:
        lang = json.loads(mod.read('assets/apocalypsenow/lang/en_us.json'))
    ids = sorted(k.removeprefix('entity.apocalypsenow.') for k in lang
                 if re.fullmatch(r'entity\.apocalypsenow\.(walker_\d+|runner_\d+|horde_\d+)', k))
    expected = {f'walker_{i}' for i in range(1, 34)} | {f'runner_{i}' for i in range(34, 58)} | {f'horde_{i}' for i in range(1, 6)}
    if set(ids) != expected:
        raise ValueError('IDs diferentes do Apocalypse Now 3.0.5 esperado; revise a compatibilidade antes de gerar.')
    pattern = 'regex:apocalypsenow:(' + '|'.join(ids) + ')'
    properties = '# Generated for Lazarus. Other entities retain the default model.\nmodels.1=2\nnbt.1.id=' + pattern + '\n\nmodels.2=1\n'
    files = {'pack.mcmeta': json.dumps({'pack': {'pack_format': 15, 'description': 'Lazarus | Apocalypse Reanimated Compat (experimental)'}}, ensure_ascii=False)}
    with zipfile.ZipFile(reanimated) as source:
        for target, original in [('player', 'zombie'), ('player_inner_armor', 'zombie_inner_armor'), ('player_outer_armor', 'zombie_outer_armor')]:
            model = json.loads(source.read(f'assets/minecraft/optifine/cem/{original}.jem'))
            if 'texture' in model:
                raise ValueError(f'{original}: textura explicita nao esperada; revise o modelo antes de gerar.')
            files[f'assets/minecraft/optifine/cem/{target}2.jem'] = json.dumps(model, ensure_ascii=False)
            files[f'assets/minecraft/optifine/cem/{target}.properties'] = properties
    files['LEIA-ME.txt'] = ('Patch experimental gerado de arquivos locais do Reanimated Blue. Requer EMF e ETF.\n'
                           'Cobertura: 33 Walkers, 24 Runners, 5 Hordes. Crawlers fora do escopo.\n'
                           'Ative acima do Reanimated e do Tissou. Validacao visual pendente.\n'
                           'Verifique as permissoes dos autores antes de redistribuir este ZIP.\n')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, content.encode('utf-8'))
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError('Falha de integridade no ZIP gerado.')
        for name in archive.namelist():
            if name.endswith(('.jem', '.mcmeta')):
                json.loads(archive.read(name))
    print(f'Gerado: {output.resolve()} | {len(ids)} IDs | JSON/ZIP validos')
    print('SHA256:', hashlib.sha256(output.read_bytes()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instance', type=Path)
    parser.add_argument('--apocalypse', type=Path)
    parser.add_argument('--reanimated', type=Path)
    parser.add_argument('--output', type=Path, default=Path('dist/Lazarus - Apocalypse Reanimated Compat.zip'))
    args = parser.parse_args()
    try:
        if args.instance:
            args.apocalypse = args.apocalypse or select_one(args.instance / 'mods', 'apocalypsenow-*.jar')
            args.reanimated = args.reanimated or select_one(args.instance / 'resourcepacks', '*Reanimated*.zip')
        if not args.apocalypse or not args.reanimated:
            parser.error('Informe --instance ou ambos --apocalypse e --reanimated.')
        build(args.apocalypse, args.reanimated, args.output)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f'Erro: {error}\n')


if __name__ == '__main__':
    main()
