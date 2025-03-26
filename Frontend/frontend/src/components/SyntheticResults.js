import React from 'react';
import { Table, Card, Tag, Typography, Statistic, Row, Col } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';

const { Title } = Typography;

const SyntheticResults = ({ data }) => {
  if (!data || !data.length) return null;

  const columns = [
    {
      title: 'Entry Type',
      key: 'type',
      render: (_, record, index) => (
        <Tag color={record.is_defaulter ? 'red' : 'green'} icon={record.is_defaulter ? <CloseCircleOutlined /> : <CheckCircleOutlined />}>
          {record.is_defaulter ? 'Defaulter' : 'Non-Defaulter'}
        </Tag>
      ),
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
    },
    {
      title: 'Income',
      dataIndex: 'income',
      key: 'income',
      render: (income) => `₹${income.toLocaleString('en-IN')}`,
    },
    {
      title: 'Experience',
      dataIndex: 'experience',
      key: 'experience',
      render: (exp) => `${exp} years`,
    },
    {
      title: 'Current Job',
      dataIndex: 'current_job_years',
      key: 'current_job_years',
      render: (years) => `${years} years`,
    },
    {
      title: 'Current House',
      dataIndex: 'current_house_years',
      key: 'current_house_years',
      render: (years) => `${years} years`,
    },
    {
      title: 'Home Ownership',
      dataIndex: 'home_ownership',
      key: 'home_ownership',
      render: (status) => (
        <Tag color={status === 'owned' ? 'green' : status === 'rented' ? 'blue' : 'orange'}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </Tag>
      ),
    },
    {
      title: 'Car Ownership',
      dataIndex: 'car_ownership',
      key: 'car_ownership',
      render: (status) => (
        <Tag color={status === 'yes' ? 'green' : 'red'}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Profession',
      dataIndex: 'profession',
      key: 'profession',
      render: (prof) => prof.replace(/_/g, ' '),
    },
    {
      title: 'State',
      dataIndex: 'state',
      key: 'state',
      render: (state) => state.charAt(0).toUpperCase() + state.slice(1),
    },
  ];

  const defaulters = data.filter(entry => entry.is_defaulter);
  const nonDefaulters = data.filter(entry => !entry.is_defaulter);

  return (
    <Card>
      <Title level={4}>Generated Synthetic Data</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Statistic
            title="Total Records"
            value={data.length}
          />
        </Col>
        <Col span={8}>
          <Statistic
            title="Defaulters"
            value={defaulters.length}
            valueStyle={{ color: '#cf1322' }}
            suffix={`/ ${data.length}`}
          />
        </Col>
        <Col span={8}>
          <Statistic
            title="Non-Defaulters"
            value={nonDefaulters.length}
            valueStyle={{ color: '#3f8600' }}
            suffix={`/ ${data.length}`}
          />
        </Col>
      </Row>

      <Table
        columns={columns}
        dataSource={data.map((entry, index) => ({ ...entry, key: index }))}
        scroll={{ x: true }}
        pagination={{
          defaultPageSize: 5,
          showSizeChanger: true,
          showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} entries`,
        }}
      />
    </Card>
  );
};

export default SyntheticResults; 