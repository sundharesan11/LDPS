import React, { useState } from 'react';
import { Card, Button, InputNumber, Slider, Row, Col, Space, Divider } from 'antd';

const SyntheticGenerator = ({ onGenerate }) => {
  const [count, setCount] = useState(1);
  const [defaultRatio, setDefaultRatio] = useState(0.3);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      await onGenerate(count, defaultRatio);
    } catch (error) {
      console.error('Error in synthetic generation:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Synthetic Data Generator" bordered={false}>
      <Row gutter={16}>
        <Col span={12}>
          <div style={{ marginBottom: 16 }}>
            <div>Number of Records</div>
            <InputNumber
              min={1}
              max={100}
              value={count}
              onChange={setCount}
              style={{ width: '100%' }}
            />
          </div>
        </Col>
        <Col span={12}>
          <div style={{ marginBottom: 16 }}>
            <div>Default Ratio</div>
            <Slider
              min={0}
              max={1}
              step={0.1}
              value={defaultRatio}
              onChange={setDefaultRatio}
              marks={{
                0: '0%',
                0.5: '50%',
                1: '100%'
              }}
            />
          </div>
        </Col>
      </Row>
      
      <Divider />
      
      <Button 
        type="primary" 
        onClick={handleGenerate} 
        loading={loading}
        block
      >
        Generate Synthetic Data
      </Button>
    </Card>
  );
};

export default SyntheticGenerator;