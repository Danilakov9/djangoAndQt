#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QSerialPort>
#include <QString>

QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();
    QSerialPort *serialport;  //声明一个串口

private slots:
    void on_serial_open_clicked();

    void on_serial_close_clicked();

    void serial_textedit_slot();

    void on_pushButton_clicked();
    void on_pushButton_2_clicked();



    void on_temp_high_send_clicked();

    void on_sun_high_send_clicked();

private:
    Ui::Widget *ui;
};
#endif // WIDGET_H
