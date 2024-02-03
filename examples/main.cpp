#include <QMap>
#include <QString>

int main() {
    auto hello = QString("Hello World");
    auto demosthenes = QString("Οὐχὶ ταὐτὰ παρίσταταί μοι γιγνώσκειν, ὦ ἄνδρες ᾿Αθηναῖοι");

    auto map = QMap<QString , uint32_t>{
            {"one", 1},
            {"forty-two", 42},
            {"1.21 gigawatts", 1210000}
    };

    return 0;
}