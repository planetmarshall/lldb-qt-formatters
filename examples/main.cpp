#include <QMap>
#include <QString>

int main() {
    auto hello = QString("Hello World");
    auto demosthenes = QString("Οὐχὶ ταὐτὰ παρίσταταί μοι γιγνώσκειν, ὦ ἄνδρες ᾿Αθηναῖοι");

    auto map = QMap<QString , uint32_t>{};
    map["one"] = 1;
    map["forty-two"] = 42;
    map["1.21 gigawatts"] = 1210000;

    return 0;
}