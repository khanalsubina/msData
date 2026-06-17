import sys
import importlib
from importlib.metadata import version, PackageNotFoundError

try:
    from packaging.version import parse as parse_version
except ImportError:
    raise ImportError(
        "The 'packaging' library is required for version comparison.\n"
        "Install it with: pip install packaging"
    )


# Required minimum versions
REQUIRED = {
    "python": {"min_version": "3.9", "display": "Python", "module": None},
    "pandas": {"min_version": "2.1", "display": "pandas", "module": "pandas"},
    "numpy": {"min_version": "1.24", "display": "numpy", "module": "numpy"},
    "scikit-learn": {"min_version": "1.5", "display": "scikit-learn", "module": "sklearn"},
    "tensorflow": {"min_version": "2.17", "display": "tensorflow", "module": "tensorflow"},
    "torch": {"min_version": "2.10.0", "display": "torch", "module": "torch"},
    "scipy": {"min_version": "1.10", "display": "scipy", "module": "scipy"},
    "xgboost": {"min_version": "3.0", "display": "xgboost", "module": "xgboost"},
    "transformers": {"min_version": "4.50", "display": "transformers", "module": "transformers"},
    "autogluon": {"min_version": "1.1", "display": "autogluon", "module": "autogluon"},
    "tf-keras": {"min_version": "2.15", "display": "tf-keras", "module": "tf_keras"},
    "granite-tsfm": {"min_version": "0.1", "display": "granite-tsfm", "module": None},
    "matplotlib": {"min_version": "3.8", "display": "matplotlib", "module": "matplotlib"},
    "river": {"min_version": "0.20", "display": "river", "module": "river"},
}


def check_python():
    py_version = ".".join(map(str, sys.version_info[:3]))
    min_version = REQUIRED["python"]["min_version"]

    if parse_version(py_version) >= parse_version(min_version):
        print(f"Python: {py_version} (OK, >= {min_version})")
    else:
        print(f"Python: {py_version} (TOO OLD, need >= {min_version})")


def check_package(dist_name, display_name, min_version, module_name=None):
    try:
        installed_version = version(dist_name)

        if parse_version(installed_version) >= parse_version(min_version):
            print(f"{display_name}: {installed_version} (OK, >= {min_version})")
        else:
            print(f"{display_name}: {installed_version} (TOO OLD, need >= {min_version})")

        # Optional import check if module name is known
        if module_name:
            try:
                importlib.import_module(module_name)
            except Exception as e:
                print(f"  ! Import warning for {display_name}: {e}")

    except PackageNotFoundError:
        print(f"✗ {display_name}: not installed (need >= {min_version})")


def main():
    print("=== Environment Version Check ===")
    print()

    check_python()
    print()

    for dist_name, info in REQUIRED.items():
        if dist_name == "python":
            continue
        check_package(
            dist_name=dist_name,
            display_name=info["display"],
            min_version=info["min_version"],
            module_name=info["module"],
        )

    print()
    print("Done.")


if __name__ == "__main__":
    main()