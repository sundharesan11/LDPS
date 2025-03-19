import React, { useState, useEffect } from 'react';
import { Form, Input, Select, Button, Slider, InputNumber, Card, Row, Col, Divider } from 'antd';

const { Option } = Select;

const DataEntryForm = ({ onSubmit, initialData }) => {
  const [form] = Form.useForm();
  
  useEffect(() => {
    if (initialData) {
      form.setFieldsValue(initialData);
    }
  }, [initialData, form]);

  const onFinish = (values) => {
    onSubmit(values);
  };

  const onReset = () => {
    form.resetFields();
  };

  return (
    <Card title="Loan Application Data" bordered={false}>
      <Form
        form={form}
        name="loanApplication"
        layout="vertical"
        onFinish={onFinish}
        initialValues={{
          age: 35,
          income: 60000,
          loan_amount: 15000,
          loan_term: 36,
          credit_score: 720,
          employment_years: 5,
          debt_to_income: 0.3,
          home_ownership: "MORTGAGE",
          education: "BACHELOR",
          marital_status: "MARRIED"
        }}
      >
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="age"
              label="Age"
              rules={[{ required: true, message: 'Please input age!' }]}
            >
              <InputNumber min={18} max={100} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="income"
              label="Annual Income ($)"
              rules={[{ required: true, message: 'Please input income!' }]}
            >
              <InputNumber 
                min={0} 
                step={1000} 
                formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value.replace(/\$\s?|(,*)/g, '')}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="loan_amount"
              label="Loan Amount ($)"
              rules={[{ required: true, message: 'Please input loan amount!' }]}
            >
              <InputNumber 
                min={1000} 
                step={1000} 
                formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value.replace(/\$\s?|(,*)/g, '')}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
        </Row>
        
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="loan_term"
              label="Loan Term (months)"
              rules={[{ required: true, message: 'Please select loan term!' }]}
            >
              <Select>
                <Option value={12}>12 months</Option>
                <Option value={24}>24 months</Option>
                <Option value={36}>36 months</Option>
                <Option value={48}>48 months</Option>
                <Option value={60}>60 months</Option>
              </Select>
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="credit_score"
              label="Credit Score"
              rules={[{ required: true, message: 'Please input credit score!' }]}
            >
              <Slider
                min={300}
                max={850}
                marks={{
                  300: '300',
                  550: '550',
                  700: '700',
                  850: '850'
                }}
              />
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="employment_years"
              label="Years of Employment"
              rules={[{ required: true, message: 'Please input employment years!' }]}
            >
              <InputNumber min={0} max={50} step={0.5} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
        
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="debt_to_income"
              label="Debt-to-Income Ratio"
              rules={[{ required: true, message: 'Please input debt-to-income ratio!' }]}
            >
              <Slider
                min={0}
                max={1}
                step={0.01}
                marks={{
                  0: '0',
                  0.2: '0.2',
                  0.4: '0.4',
                  0.6: '0.6',
                  0.8: '0.8',
                  1: '1'
                }}
              />
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="home_ownership"
              label="Home Ownership"
              rules={[{ required: true, message: 'Please select home ownership status!' }]}
            >
              <Select>
                <Option value="OWN">Own</Option>
                <Option value="MORTGAGE">Mortgage</Option>
                <Option value="RENT">Rent</Option>
              </Select>
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="education"
              label="Education Level"
              rules={[{ required: true, message: 'Please select education level!' }]}
            >
              <Select>
                <Option value="HIGH_SCHOOL">High School</Option>
                <Option value="BACHELOR">Bachelor's Degree</Option>
                <Option value="MASTER">Master's Degree</Option>
                <Option value="PHD">PhD</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>
        
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="marital_status"
              label="Marital Status"
              rules={[{ required: true, message: 'Please select marital status!' }]}
            >
              <Select>
                <Option value="SINGLE">Single</Option>
                <Option value="MARRIED">Married</Option>
                <Option value="DIVORCED">Divorced</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>
        
        <Divider />
        
        <Form.Item>
          <Button type="primary" htmlType="submit" style={{ marginRight: '8px' }}>
            Predict Default Risk
          </Button>
          <Button htmlType="button" onClick={onReset}>
            Reset Form
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default DataEntryForm;