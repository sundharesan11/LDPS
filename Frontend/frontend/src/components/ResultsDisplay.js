import React from 'react';
import { Card, Row, Col, Statistic, Divider, Progress, Table, Tag } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, BarChartOutlined } from '@ant-design/icons';

const ResultsDisplay = ({ results, applicationData }) => {
  if (!results) return null;
  
  const getDefaultStatus = (prediction) => {
    return prediction === 1 ? (
      <Tag color="red" icon={<CloseCircleOutlined />}>
        Likely to Default
      </Tag>
    ) : (
      <Tag color="green" icon={<CheckCircleOutlined />}>
        Unlikely to Default
      </Tag>
    );
  };
  
  const modelColumns = [
    {
      title: 'Model',
      dataIndex: 'model',
      key: 'model',
    },
    {
      title: 'Prediction',
      dataIndex: 'prediction',
      key: 'prediction',
      render: (prediction) => getDefaultStatus(prediction)
    },
  ];
  
  const modelData = [
    {
      key: '1',
      model: 'Random Forest (Model 1)',
      prediction: results.model1_prediction,
    },
    {
      key: '2',
      model: 'XGBoost (Model 2)',
      prediction: results.model2_prediction,
    },
    {
      key: '3',
      model: 'Neural Network (Model 3)',
      prediction: results.model3_prediction,
    },
  ];
  
  // Prepare feature importance data if available
  const featureImportanceData = results.feature_importance ? 
    Object.entries(results.feature_importance)
      .map(([feature, importance], index) => ({
        key: index,
        feature: feature.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
        importance: importance,
      }))
      .sort((a, b) => b.importance - a.importance)
      .slice(0, 5) : [];
  
  const featureColumns = [
    {
      title: 'Feature',
      dataIndex: 'feature',
      key: 'feature',
    },
    {
      title: 'Importance',
      dataIndex: 'importance',
      key: 'importance',
      render: (importance) => (
        <Progress 
          percent={Math.round(importance * 100)} 
          size="small" 
          format={(percent) => `${percent}%`}
        />
      ),
    },
  ];

  return (
    <Card 
      title={
        <div>
          Prediction Results
          {results.ensemble_prediction === 1 ? (
            <Tag color="red" style={{ marginLeft: 16 }}>
              High Risk
            </Tag>
          ) : (
            <Tag color="green" style={{ marginLeft: 16 }}>
              Low Risk
            </Tag>
          )}
        </div>
      } 
      bordered={false}
    >
      <Row gutter={16}>
        <Col span={12}>
          <Statistic
            title="Default Probability"
            value={results.default_probability * 100}
            precision={2}
            suffix="%"
            valueStyle={{
              color: results.default_probability > 0.5 ? '#cf1322' : '#3f8600',
            }}
          />
          
          <Progress
            percent={Math.round(results.default_probability * 100)}
            status={results.default_probability > 0.5 ? "exception" : "success"}
            strokeWidth={20}
            style={{ marginTop: 16 }}
          />
        </Col>
        
        <Col span={12}>
          <Statistic
            title="Ensemble Prediction"
            value={results.ensemble_prediction === 1 ? "Default" : "No Default"}
            valueStyle={{
              color: results.ensemble_prediction === 1 ? '#cf1322' : '#3f8600',
            }}
          />
          <div style={{ marginTop: 24 }}>
            <BarChartOutlined style={{ fontSize: 24, marginRight: 8 }} />
            <span>Based on majority vote from 3 models</span>
          </div>
        </Col>
      </Row>
      
      <Divider>Individual Model Predictions</Divider>
      
      <Table 
        columns={modelColumns} 
        dataSource={modelData} 
        pagination={false}
        size="small"
      />
      
      {featureImportanceData.length > 0 && (
        <>
          <Divider>Top 5 Important Features</Divider>
          <Table 
            columns={featureColumns} 
            dataSource={featureImportanceData} 
            pagination={false}
            size="small"
          />
        </>
      )}
    </Card>
  );
};

export default ResultsDisplay;