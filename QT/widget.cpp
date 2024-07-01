#include "widget.h"
#include "ui_widget.h"
#include <QSerialPortInfo>
#include <QMessageBox>
#include <QTime>
#include <QTimer>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QFile>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);

    //start
    serialport = new QSerialPort(this);
    //自动获取串口名称
    QStringList serialPortName;
    foreach(const QSerialPortInfo &info,QSerialPortInfo::availablePorts()){
        serialPortName<<info.portName();
    }
    ui->serial_com->addItems(serialPortName); //在控件显示串口名称
    //connect
    connect(serialport,SIGNAL(readyRead()),this,SLOT(serial_textedit_slot()));
}

Widget::~Widget()
{
    delete ui;
}

QJsonObject tempData;  // 临时存储数据
QString currentTimestamp;  // 临时存储时间戳

//触发槽函数，显示串口打印信息
void Widget::serial_textedit_slot()
{
    if (currentTimestamp.isEmpty()) {
        QTime current_time = QTime::currentTime(); //获取系统时间
        currentTimestamp = current_time.toString("hh:mm:ss"); //格式化数据时间
    }

    QString buf, dhtbuf, str_t, str_h, str_s, str_id;
    buf = QString(serialport->readAll());
    dhtbuf.append(buf);

    bool hasNewData = false;
    if (dhtbuf.at(0) == QChar('T'))
    {
        str_t.append(dhtbuf.at(1));
        str_t.append(dhtbuf.at(2));
        ui->serial_dht_wendu->setText(str_t);
        str_h.append(dhtbuf.at(3));
        str_h.append(dhtbuf.at(4));
        ui->serial_dht_shidu->setText(str_h);
        str_s.append(dhtbuf.at(5));
        str_s.append(dhtbuf.at(6));
        ui->serial_gas->setText(str_s);

        tempData["Temperature"] = str_t;
        tempData["Humidity"] = str_h;
        tempData["Gas"] = str_s;
        hasNewData = true;
    }
    else if (dhtbuf.at(0) == 'I')
    {
        str_id.append(dhtbuf.at(1));
        str_id.append(dhtbuf.at(2));
        str_id.append(dhtbuf.at(3));
        str_id.append(dhtbuf.at(4));
        str_id.append(dhtbuf.at(5));
        str_id.append(dhtbuf.at(6));
        str_id.append(dhtbuf.at(7));
        str_id.append(dhtbuf.at(8));
        ui->serial_id->setText(str_id);

        tempData["ID"] = str_id;
        hasNewData = true;
    }

    if (hasNewData)
    {
        if (tempData.contains("Temperature") && tempData.contains("ID"))
        {
            QString str_sq_buf;
            str_sq_buf.append(currentTimestamp);
            str_sq_buf.append(" 温度:");
            str_sq_buf.append(ui->serial_dht_wendu->text());
            str_sq_buf.append(" 湿度:");
            str_sq_buf.append(ui->serial_dht_shidu->text());
            str_sq_buf.append(" 烟雾:");
            str_sq_buf.append(ui->serial_gas->text());
            str_sq_buf.append(" ID:");
            str_sq_buf.append(ui->serial_id->text());

            ui->serial_rx_edit->appendPlainText(str_sq_buf);

            // 添加时间戳到JSON对象
            tempData["Timestamp"] = currentTimestamp;

            // 读取现有文件内容
            QFile jsonFile("data.json");
            QJsonArray jsonArray;

            if (jsonFile.exists() && jsonFile.open(QIODevice::ReadOnly))
            {
                QByteArray fileData = jsonFile.readAll();
                QJsonDocument loadDoc(QJsonDocument::fromJson(fileData));
                if (loadDoc.isArray())
                {
                    jsonArray = loadDoc.array();
                }
                jsonFile.close();
            }

            // 添加新记录
            jsonArray.append(tempData);

            // 写回文件
            if (jsonFile.open(QIODevice::WriteOnly))
            {
                QJsonDocument saveDoc(jsonArray);
                jsonFile.write(saveDoc.toJson(QJsonDocument::Indented));
                jsonFile.close();
            }

            // 清空临时数据和时间戳
            tempData = QJsonObject();
            currentTimestamp.clear();
        }
    }
}
//串口初始化参数配置
void Widget::on_serial_open_clicked()
{
    QSerialPort::BaudRate baudrate;
    QSerialPort::DataBits databits;
    QSerialPort::StopBits stopbits;
    QSerialPort::Parity check;
    //波特率
    if (ui->serial_baud->currentText() == "9600")
    {
        baudrate = QSerialPort::Baud9600;
    }
    else if (ui->serial_baud->currentText() == "38400")
    {
        baudrate = QSerialPort::Baud38400;
    }
    else if (ui->serial_baud->currentText() == "115200")
    {
        baudrate = QSerialPort::Baud115200;
    }
    //数据位
    if (ui->serial_data->currentText() == "5")
    {
        databits = QSerialPort::Data5;
    }
    else if (ui->serial_data->currentText() == "6")
    {
        databits = QSerialPort::Data6;
    }
    else if (ui->serial_data->currentText() == "7")
    {
        databits = QSerialPort::Data7;
    }
    else if (ui->serial_data->currentText() == "8")
    {
        databits = QSerialPort::Data8;
    }
    //停止位
    if (ui->serial_stop->currentText() == "1")
    {
        stopbits = QSerialPort::OneStop;
    }
    else if (ui->serial_stop->currentText() == "1.5")
    {
        stopbits = QSerialPort::OneAndHalfStop;
    }
    else if (ui->serial_stop->currentText() == "2")
    {
        stopbits = QSerialPort::TwoStop;
    }
    //校验位
    if (ui->serial_check->currentText() == "none")
    {
        check = QSerialPort::NoParity;
    }
    //初始化
    serialport->setPortName(ui->serial_com->currentText());
    serialport->setBaudRate(baudrate);
    serialport->setDataBits(databits);
    serialport->setStopBits(stopbits);
    serialport->setParity(check);
    //判断是否打开成功
    if (serialport->open(QIODevice::ReadWrite) == true)
    {
        QMessageBox::information(this, "提示", "成功");
    }
    else
    {
        QMessageBox::critical(this, "提示", "错误");
    }
}

void Widget::on_serial_close_clicked()
{
    serialport->close();
}

void Widget::on_pushButton_clicked()
{
    // serialport->write(ui->serial_tx_edit->text().toLocal8Bit().data());
}

void Widget::on_pushButton_2_clicked()
{
    // ui->serial_rx_edit->clear();
}

//温度阈值设置
void Widget::on_temp_high_send_clicked()
{
    QString buf;
    buf = 'D';
    buf.append(ui->temp_high->text());
    serialport->write(buf.toLocal8Bit().data());
}
//气体阈值设置
void Widget::on_sun_high_send_clicked()
{
    QString buf;
    buf = 'G';
    buf.append(ui->gas_high->text());
    serialport->write(buf.toLocal8Bit().data());
}
