"""Reproducible COLMAP experiments; preserves original image bytes."""
import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXT = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp'}


def images(folder):
    files = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXT)
    unsupported = [p.name for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {'.heic', '.heif', '.dng'}]
    if unsupported:
        raise ValueError('Formato da gestire prima della ricostruzione, conservando gli originali: ' + ', '.join(unsupported))
    return files


def prepare():
    baseline = images(ROOT / 'originals/baseline')
    broken = images(ROOT / 'originals/broken')
    extra = images(ROOT / 'originals/repair_extra')
    if len(baseline) != 20 or not 2 <= len(broken) <= 10 or not 1 <= len(extra) <= 3:
        raise ValueError(f'Servono 20 baseline, 2-10 broken, 1-3 repair_extra; trovati {len(baseline)}, {len(broken)}, {len(extra)}.')
    order = ROOT / 'baseline_order.txt'
    if order.exists():
        names = [s.strip() for s in order.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
        if len(names) != 20 or set(names) != {p.name for p in baseline}:
            raise ValueError('baseline_order.txt deve elencare ciascuna delle 20 foto esattamente una volta.')
        baseline = [ROOT / 'originals/baseline' / n for n in names]
    sets = {f'baseline_{n:02}': [baseline[i * 20 // n] for i in range(n)] for n in (20, 10, 5, 3)}
    sets.update(broken=broken, repaired=broken + extra)
    target = ROOT / 'experiments'
    if target.exists():
        raise ValueError('experiments esiste gia: preservato. Usa una nuova copia del progetto per nuovi dati.')
    target.mkdir()
    manifest = {}
    for name, paths in sets.items():
        folder = target / name / 'images'
        folder.mkdir(parents=True)
        manifest[name] = []
        for source in paths:
            dest = folder / (source.parent.name + '_' + source.name)
            shutil.copy2(source, dest)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if hashlib.sha256(dest.read_bytes()).hexdigest() != digest:
                raise ValueError('Copia non integra: ' + str(dest))
            manifest[name].append({'source': str(source.relative_to(ROOT)), 'file': dest.name, 'sha256': digest})
    (target / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Preparati sei esperimenti, originali preservati.')


def execute(command, log):
    # Windows batch launchers are handled by subprocess on Windows.
    with log.open('w', encoding='utf-8') as output:
        result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, check=False)
    return result.returncode


def count_binary(path):
    with path.open('rb') as stream:
        return struct.unpack('<Q', stream.read(8))[0]


def run(colmap):
    executable = shutil.which(colmap) or (str(Path(colmap).resolve()) if Path(colmap).is_file() else None)
    if not executable:
        raise ValueError('COLMAP non trovato: specifica --colmap con il percorso di COLMAP.bat o colmap.exe.')
    target = ROOT / 'experiments'
    manifest = json.loads((target / 'manifest.json').read_text(encoding='utf-8'))
    execute([executable, '-h'], target / 'colmap_version_help.txt')
    results_path = target / 'results.json'
    results = json.loads(results_path.read_text(encoding='utf-8')) if results_path.exists() else {}
    for name in manifest:
        folder = target / name
        workspace = folder / 'workspace'
        if workspace.exists():
            print(name + ': gia avviato, preservato.')
            continue
        workspace.mkdir()
        command = [executable, 'automatic_reconstructor', '--workspace_path', str(workspace), '--image_path', str(folder / 'images'), '--dense', '0']
        (folder / 'command.json').write_text(json.dumps(command, indent=2), encoding='utf-8')
        print('Esecuzione ' + name, flush=True)
        code = execute(command, folder / 'run.log')
        components = []
        for model in sorted((workspace / 'sparse').glob('*')):
            if model.is_dir() and (model / 'images.bin').exists() and (model / 'points3D.bin').exists():
                components.append({'model': str(model.relative_to(ROOT)), 'registered_images': count_binary(model / 'images.bin'), 'points3D': count_binary(model / 'points3D.bin')})
                execute([executable, 'model_analyzer', '--path', str(model)], folder / ('analysis_' + model.name + '.txt'))
        results[name] = {'input_images': len(manifest[name]), 'exit_code': code, 'status': 'execution_error' if code else ('model_produced_requires_visual_check' if components else 'no_model'), 'components': components}
        results_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print('Risultati salvati in experiments/results.json; controllare log e geometria.')


def package():
    originals = [p for p in (ROOT / 'originals').rglob('*') if p.is_file()]
    if not originals:
        raise ValueError('Nessuna immagine originale da includere.')
    destination = ROOT / 'submission'
    destination.mkdir(exist_ok=True)
    with zipfile.ZipFile(destination / 'original_images.zip', 'w', compression=zipfile.ZIP_STORED) as archive:
        for path in originals:
            archive.write(path, path.relative_to(ROOT))
    print('ZIP degli originali creato senza compressione.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run', 'zip'])
    parser.add_argument('--colmap', default='colmap')
    args = parser.parse_args()
    try:
        {'prepare': prepare, 'run': lambda: run(args.colmap), 'zip': package}[args.action]()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
