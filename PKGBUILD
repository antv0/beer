# Maintainer: Your Name <your_email>

pkgname=python-beer
pkgver=0.0.1
pkgrel=1
pkgdesc="Easily manage wine prefixes"
arch=('any')
url="https://github.com/antv0/beer"  # Replace with your GitHub repository URL
license=('MIT')
depends=(
  'python>=3.11'
  'python-hatchling'
)
makedepends=(
  'python-setuptools'
  'python-pip'
)
source=("https://github.com/antv0/beer/archive/refs/tags/$pkgver.tar.gz")
sha256sums=('SKIP')

prepare() {
  cd "$srcdir/beer-$pkgver"
  sed -i "s/0.0.1/$pkgver/" pyproject.toml
}

build() {
  cd "$srcdir/beer-$pkgver"
  python -m build
}

package() {
  cd "$srcdir/beer-$pkgver"
  python -m pip install --root="$pkgdir/" --ignore-installed .
  
  # Install license and readme
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}
