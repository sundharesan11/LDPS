import React, { useState } from 'react';
import { Layout, Menu, Typography, Spin, Alert, Tabs } from 'antd';
import { 
  FormOutlined, 
  DashboardOutlined, 
  RobotOutlined,
  BarChartOutlined
} from '@ant-design/icons';

import DataEntryForm from './components/DataEntryForm';
import SyntheticGenerator from './components/SyntheticGenerator';
import ResultsDisplay from './components/ResultsDisplay';
import { predictLoanDefault, generateSyntheticData } from './services/api';

import './App.css';

const { Header, Content, Footer } = Layout;
const { Title } = Typography;
const { TabPane } = Tabs;

const App = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [predictionResults, setPredictionResults] = useState(null);
  const [applicationData, setApplicationData] = useState(null);
  const [activeTab, setActiveTab] = useState('1');

  const handlePrediction = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await predictLoanDefault(formData);
      setPredictionResults(results);
      setApplicationData(formData);
      setActiveTab('3'); // Switch to results tab
    } catch (error) {
      setError('Failed to get prediction. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSyntheticGeneration = async (count, defaultRatio) => {
    setLoading(true);
    setError(null);
    
    try {
      // Generate synthetic data
      const syntheticData = await generateSyntheticData(count, defaultRatio);
      
      if (syntheticData && syntheticData.length > 0) {
        // Use the first generated record
        const firstRecord = syntheticData[0];
        
        // Predict using this record
        const results = await predictLoanDefault(firstRecord);
        
        setPredictionResults(results);
        setApplicationData(firstRecord);
        setActiveTab('3'); // Switch to results tab
      }
    } catch (error) {
      setError('Failed to generate synthetic data. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout className="layout" style={{ minHeight: '100vh' }}>
      <Header>
        <div className="logo" />
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          <Menu.Item key="1" icon={<DashboardOutlined />}>Loan Default Prediction System</Menu.Item>
        </Menu>
      </Header>
      
      <Content style={{ padding: '0 50px', marginTop: 40 }}>
        <div className="site-layout-content" style={{ background: '#fff', padding: 24, minHeight: 380 }}>
          <Title level={2} style={{ marginBottom: 20 }}>
            <BarChartOutlined /> Financial Risk Assessment
          </Title>
          
          {error && (
            <Alert
              message="Error"
              description={error}
              type="error"
              showIcon
              closable
              style={{ marginBottom: 16 }}
            />
          )}
          
          <Spin spinning={loading} tip="Processing...">
            <Tabs activeKey={activeTab} onChange={setActiveTab}>
              <TabPane
                tab={<span><FormOutlined />Manual Data Entry</span>}
                key="1"
              >
                <DataEntryForm 
                  onSubmit={handlePrediction} 
                  initialData={applicationData}
                />
              </TabPane>
              
              <TabPane
                tab={<span><RobotOutlined />Synthetic Data</span>}
                key="2"
              >
                <SyntheticGenerator onGenerate={handleSyntheticGeneration} />
              </TabPane>
              
              <TabPane
                tab={<span><BarChartOutlined />Results</span>}
                key="3"
                disabled={!predictionResults}
              >
                <ResultsDisplay 
                  results={predictionResults} 
                  applicationData={applicationData}
                />
              </TabPane>
            </Tabs>
          </Spin>
        </div>
      </Content>
      
      <Footer style={{ textAlign: 'center' }}>
        Loan Default Prediction System ©{new Date().getFullYear()}
      </Footer>
    </Layout>
  );
};

export default App;