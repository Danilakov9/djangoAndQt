import React, { useState, useEffect } from 'react';
import { Layout, Card, Row, Col, Typography, message, Spin, Statistic, Tag, Empty, Pagination } from 'antd';
import axios from 'axios';

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

const sensorStatus = {
    '00000000': { text: '空闲00000000', color: 'default' },
    '73468616': { text: '白卡73468616', color: 'blue' },
    '7377C60C': { text: '门禁卡7377C60C', color: 'green' }
};

const App = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [paginationData, setPaginationData] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);
    const [totalItems, setTotalItems] = useState(0);

    useEffect(() => {
        fetchData();
        const interval = setInterval(() => {
            loadData();
            fetchData();
        }, 10000);
        return () => clearInterval(interval);
    }, []);

    const loadData = async () => {
        try {
            await axios.post('http://127.0.0.1:8000/load-data/');
        } catch (error) {
            message.error('Failed to load data');
        }
    };

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get('http://127.0.0.1:8000/last-sensor-data/');
            setData(response.data);
        } catch (error) {
            message.error('Failed to fetch data');
        }
        setLoading(false);
    };

    const fetchPaginatedData = async (page, size) => {
        setLoading(true);
        try {
            const response = await axios.get(`http://127.0.0.1:8000/sensor-data-paginated/?page_number=${page}&page_size=${size}`);
            setPaginationData(response.data.data);
            setTotalItems(response.data.total_items);
        } catch (error) {
            message.error('Failed to fetch paginated data');
        }
        setLoading(false);
    };



    useEffect(() => {
        fetchPaginatedData(currentPage, pageSize);
    }, [currentPage, pageSize]);

    const renderSensorTag = (sensor_id) => {
        const status = sensorStatus[sensor_id] || { text: '未知', color: 'red' };
        return <Tag color={status.color}>{status.text}</Tag>;
    };

    return (
        <Layout style={{ minHeight: '100vh', width: '100%' }}>
            <Row style={{ height: '50%' }}>
                <Col span={12} style={{ backgroundColor: '#d9d9d9', padding: '20px' }}>
                    <Spin spinning={loading} size="large">
                        <Card>
                            <Header style={{ backgroundColor: '#5e6063' }}>
                                <Title style={{ color: 'white', textAlign: 'center' }} level={2}>智能家庭环境监测系统</Title>
                            </Header>
                            <Content style={{ padding: '20px' }}>
                                <Row gutter={[16, 16]}>
                                    <Col span={8}>
                                        <Card>
                                            <Statistic
                                                title="温度"
                                                value={data ? data.temperature : '-'}
                                                suffix={data ? '°C' : ''}
                                            />
                                        </Card>
                                    </Col>
                                    <Col span={8}>
                                        <Card>
                                            <Statistic
                                                title="湿度"
                                                value={data ? data.humidity : '-'}
                                                suffix={data ? '%' : ''}
                                            />
                                        </Card>
                                    </Col>
                                    <Col span={8}>
                                        <Card>
                                            <Statistic
                                                title="气体浓度"
                                                value={data ? data.gas : '-'}
                                                suffix={data ? 'ppm' : ''}
                                            />
                                        </Card>
                                    </Col>
                                    <Col span={24}>
                                        <Card>
                                            <Typography.Title level={4}>传感器状态</Typography.Title>
                                            {data ? renderSensorTag(data.sensor_id) : '无数据'}
                                        </Card>
                                    </Col>
                                    {data && (
                                        <Col span={24}>
                                            <Card>
                                                <Typography.Text>更新时间: {data.timestamp}</Typography.Text>
                                            </Card>
                                        </Col>
                                    )}
                                </Row>
                                {!data && (
                                    <Row style={{ marginTop: '20px' }} justify="center">
                                        <Empty description="暂无数据" />
                                    </Row>
                                )}
                            </Content>
                            <Footer style={{ textAlign: 'center' }}>
                                智能家庭环境监测系统 ©2024
                            </Footer>
                        </Card>
                    </Spin>
                </Col>
                <Col span={12} style={{ backgroundColor: '#f0f2f5', padding: '20px' }}>
                    <Spin spinning={loading} size="large">
                        <Card>
                            <Typography.Title level={4}>历史数据</Typography.Title>

                            <Row gutter={[16, 16]}>
                                {paginationData.map(item => (
                                    <Col span={24} key={item.id}>
                                        <Card>
                                            <Typography.Text>传感器 ID: {item.sensor_id}</Typography.Text> -
                                            <Typography.Text>温度: {item.temperature} °C</Typography.Text> -
                                            <Typography.Text>湿度: {item.humidity} %</Typography.Text> -
                                            <Typography.Text>气体浓度: {item.gas} ppm</Typography.Text> -
                                            <Typography.Text>时间: {item.timestamp}</Typography.Text>
                                        </Card>
                                    </Col>
                                ))}
                            </Row>


                            <Pagination
                                current={currentPage}
                                pageSize={pageSize}
                                total={totalItems}
                                onChange={(page, size) => {
                                    setCurrentPage(page);
                                    setPageSize(size);
                                }}
                            />
                        </Card>
                    </Spin>
                </Col>
            </Row>
            <Row style={{ height: '50%' }}>
                <Col span={12} style={{ backgroundColor: '#fff1f0' }} />
                <Col span={12} style={{ backgroundColor: '#d6e4ff' }} />
            </Row>
        </Layout>
    );
};

export default App;
