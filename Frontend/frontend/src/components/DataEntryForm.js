import React, { useState, useEffect } from 'react';
import { Form, Input, Select, Button, InputNumber, Card, Row, Col, Divider } from 'antd';

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
          experience: 5,
          current_job_years: 2,
          current_house_years: 3,
          home_ownership: "rented",
          car_ownership: "yes",
          profession: "Engineer",
          state: "kerala"
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
              label="Annual Income (₹)"
              rules={[{ required: true, message: 'Please input income!' }]}
            >
              <InputNumber 
                min={0} 
                step={1000} 
                formatter={value => `₹ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value.replace(/₹\s?|(,*)/g, '')}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="experience"
              label="Total Experience (years)"
              rules={[{ required: true, message: 'Please input total experience!' }]}
            >
              <InputNumber min={0} max={50} step={0.5} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
        
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="current_job_years"
              label="Years in Current Job"
              rules={[{ required: true, message: 'Please input years in current job!' }]}
            >
              <InputNumber min={0} max={50} step={0.5} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="current_house_years"
              label="Years in Current House"
              rules={[{ required: true, message: 'Please input years in current house!' }]}
            >
              <InputNumber min={0} max={50} step={0.5} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="home_ownership"
              label="Home Ownership"
              rules={[{ required: true, message: 'Please select home ownership status!' }]}
            >
              <Select>
                <Option value="owned">Own</Option>
                <Option value="rented">Rent</Option>
                <Option value="noown_norent">No Own/No Rent</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>
        
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="car_ownership"
              label="Car Ownership"
              rules={[{ required: true, message: 'Please select car ownership!' }]}
            >
              <Select>
                <Option value="yes">Yes</Option>
                <Option value="no">No</Option>
              </Select>
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="profession"
              label="Profession"
              rules={[{ required: true, message: 'Please select profession!' }]}
            >
              <Select showSearch optionFilterProp="children">
                <Option value="Mechanical_engineer">Mechanical Engineer</Option>
                <Option value="Software_Developer">Software Developer</Option>
                <Option value="Technical_writer">Technical Writer</Option>
                <Option value="Civil_servant">Civil Servant</Option>
                <Option value="Librarian">Librarian</Option>
                <Option value="Economist">Economist</Option>
                <Option value="Flight_attendant">Flight Attendant</Option>
                <Option value="Architect">Architect</Option>
                <Option value="Designer">Designer</Option>
                <Option value="Physician">Physician</Option>
                <Option value="Financial_Analyst">Financial Analyst</Option>
                <Option value="Air_traffic_controller">Air Traffic Controller</Option>
                <Option value="Politician">Politician</Option>
                <Option value="Police_officer">Police Officer</Option>
                <Option value="Artist">Artist</Option>
                <Option value="Surveyor">Surveyor</Option>
                <Option value="Design_Engineer">Design Engineer</Option>
                <Option value="Chemical_engineer">Chemical Engineer</Option>
                <Option value="Hotel_Manager">Hotel Manager</Option>
                <Option value="Dentist">Dentist</Option>
                <Option value="Comedian">Comedian</Option>
                <Option value="Biomedical_Engineer">Biomedical Engineer</Option>
                <Option value="Graphic_Designer">Graphic Designer</Option>
                <Option value="Computer_hardware_engineer">Computer Hardware Engineer</Option>
                <Option value="Petroleum_Engineer">Petroleum Engineer</Option>
                <Option value="Secretary">Secretary</Option>
                <Option value="Computer_operator">Computer Operator</Option>
                <Option value="Chartered_Accountant">Chartered Accountant</Option>
                <Option value="Technician">Technician</Option>
                <Option value="Microbiologist">Microbiologist</Option>
                <Option value="Fashion_Designer">Fashion Designer</Option>
                <Option value="Aviator">Aviator</Option>
                <Option value="Psychologist">Psychologist</Option>
                <Option value="Magistrate">Magistrate</Option>
                <Option value="Lawyer">Lawyer</Option>
                <Option value="Firefighter">Firefighter</Option>
                <Option value="Engineer">Engineer</Option>
                <Option value="Official">Official</Option>
                <Option value="Analyst">Analyst</Option>
                <Option value="Geologist">Geologist</Option>
                <Option value="Drafter">Drafter</Option>
                <Option value="Statistician">Statistician</Option>
                <Option value="Web_designer">Web Designer</Option>
                <Option value="Consultant">Consultant</Option>
                <Option value="Chef">Chef</Option>
                <Option value="Army_officer">Army Officer</Option>
                <Option value="Surgeon">Surgeon</Option>
                <Option value="Scientist">Scientist</Option>
                <Option value="Civil_engineer">Civil Engineer</Option>
                <Option value="Industrial_Engineer">Industrial Engineer</Option>
                <Option value="Technology_specialist">Technology Specialist</Option>
              </Select>
            </Form.Item>
          </Col>
          
          <Col span={8}>
            <Form.Item
              name="state"
              label="State"
              rules={[{ required: true, message: 'Please select state!' }]}
            >
              <Select showSearch optionFilterProp="children">
                <Option value="madhya pradesh">Madhya Pradesh</Option>
                <Option value="maharashtra">Maharashtra</Option>
                <Option value="kerala">Kerala</Option>
                <Option value="odisha">Odisha</Option>
                <Option value="tamil nadu">Tamil Nadu</Option>
                <Option value="gujarat">Gujarat</Option>
                <Option value="rajasthan">Rajasthan</Option>
                <Option value="telangana">Telangana</Option>
                <Option value="bihar">Bihar</Option>
                <Option value="andhra pradesh">Andhra Pradesh</Option>
                <Option value="west bengal">West Bengal</Option>
                <Option value="haryana">Haryana</Option>
                <Option value="puducherry">Puducherry</Option>
                <Option value="karnataka">Karnataka</Option>
                <Option value="uttar pradesh">Uttar Pradesh</Option>
                <Option value="himachal pradesh">Himachal Pradesh</Option>
                <Option value="punjab">Punjab</Option>
                <Option value="tripura">Tripura</Option>
                <Option value="uttarakhand">Uttarakhand</Option>
                <Option value="jharkhand">Jharkhand</Option>
                <Option value="mizoram">Mizoram</Option>
                <Option value="assam">Assam</Option>
                <Option value="jammu and kashmir">Jammu and Kashmir</Option>
                <Option value="delhi">Delhi</Option>
                <Option value="chhattisgarh">Chhattisgarh</Option>
                <Option value="chandigarh">Chandigarh</Option>
                <Option value="manipur">Manipur</Option>
                <Option value="sikkim">Sikkim</Option>
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