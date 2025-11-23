import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

const AnalyticsChart = ({ type, data, title, height = 300 }) => {
  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  const renderBarChart = () => (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="name" 
          tick={{ fontSize: 12 }}
          angle={-45}
          textAnchor="end"
          height={60}
        />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#f8fafc', 
            border: '1px solid #e2e8f0',
            borderRadius: '6px'
          }}
        />
        <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );

  const renderLineChart = () => (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="name" 
          tick={{ fontSize: 12 }}
        />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#f8fafc', 
            border: '1px solid #e2e8f0',
            borderRadius: '6px'
          }}
        />
        <Line 
          type="monotone" 
          dataKey="value" 
          stroke="#3B82F6" 
          strokeWidth={2}
          dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
          activeDot={{ r: 6, stroke: '#3B82F6', strokeWidth: 2 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );

  const renderPieChart = () => (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#f8fafc', 
            border: '1px solid #e2e8f0',
            borderRadius: '6px'
          }}
        />
      </PieChart>
    </ResponsiveContainer>
  );

  const renderPerformanceDistribution = () => {
    const performanceData = [
      { name: 'Excellent (90%+)', value: data.excellent || 0, color: '#10B981' },
      { name: 'Good (80-89%)', value: data.good || 0, color: '#3B82F6' },
      { name: 'Satisfactory (70-79%)', value: data.satisfactory || 0, color: '#F59E0B' },
      { name: 'Needs Improvement (<70%)', value: data.needs_improvement || 0, color: '#EF4444' }
    ];

    return (
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={performanceData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="name" 
            tick={{ fontSize: 10 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#f8fafc', 
              border: '1px solid #e2e8f0',
              borderRadius: '6px'
            }}
          />
          <Bar 
            dataKey="value" 
            radius={[4, 4, 0, 0]}
            fill={(entry) => entry.color}
          >
            {performanceData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    );
  };

  const renderProgressChart = () => {
    const progressData = data.map((item, index) => ({
      ...item,
      date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }));

    return (
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={progressData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            domain={[0, 100]}
            label={{ value: 'Score (%)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#f8fafc', 
              border: '1px solid #e2e8f0',
              borderRadius: '6px'
            }}
            formatter={(value) => [`${value}%`, 'Score']}
          />
          <Line 
            type="monotone" 
            dataKey="score_percentage" 
            stroke="#3B82F6" 
            strokeWidth={3}
            dot={{ fill: '#3B82F6', strokeWidth: 2, r: 5 }}
            activeDot={{ r: 7, stroke: '#3B82F6', strokeWidth: 2 }}
          />
        </LineChart>
      </ResponsiveContainer>
    );
  };

  const renderChart = () => {
    switch (type) {
      case 'bar':
        return renderBarChart();
      case 'line':
        return renderLineChart();
      case 'pie':
        return renderPieChart();
      case 'performance':
        return renderPerformanceDistribution();
      case 'progress':
        return renderProgressChart();
      default:
        return renderBarChart();
    }
  };

  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <div className="flex items-center justify-center h-64 text-gray-500">
          <div className="text-center">
            <div className="text-4xl mb-2">📊</div>
            <p>No data available</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      {/* Chart Legend for Performance Distribution */}
      {type === 'performance' && (
        <div className="flex flex-wrap gap-4 mb-4 text-sm">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded mr-2"></div>
            <span>Excellent (90%+)</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-blue-500 rounded mr-2"></div>
            <span>Good (80-89%)</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-yellow-500 rounded mr-2"></div>
            <span>Satisfactory (70-79%)</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-red-500 rounded mr-2"></div>
            <span>Needs Improvement (&lt;70%)</span>
          </div>
        </div>
      )}
      
      <div className="w-full">
        {renderChart()}
      </div>

      {/* Summary Stats */}
      {type === 'performance' && (
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-center text-sm">
          <div>
            <div className="text-lg font-semibold text-green-600">{data.excellent || 0}</div>
            <div className="text-gray-500">Excellent</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-blue-600">{data.good || 0}</div>
            <div className="text-gray-500">Good</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-yellow-600">{data.satisfactory || 0}</div>
            <div className="text-gray-500">Satisfactory</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-red-600">{data.needs_improvement || 0}</div>
            <div className="text-gray-500">Needs Work</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalyticsChart;