#!/usr/bin/env node
// Simple test to debug heatmap issues

const axios = require('axios');

async function testHeatmapData() {
  console.log('🔍 Testing heatmap data...');
  
  try {
    // Test 1: Basic API call
    console.log('📊 Testing basic API call...');
    const response = await axios.get('http://localhost:3001/api/events');
    console.log(`✅ API returned ${response.data.length} events`);
    
    // Test 2: Check for 2025 events
    console.log('📅 Checking for 2025 events...');
    const events2025 = response.data.filter(event => event.start_date.startsWith('2025'));
    console.log(`✅ Found ${events2025.length} events in 2025`);
    
    // Test 3: Check event distribution
    console.log('📊 Checking event distribution...');
    const dateCounts = {};
    events2025.slice(0, 50).forEach(event => {
      const date = event.start_date.substring(0, 10); // YYYY-MM-DD
      dateCounts[date] = (dateCounts[date] || 0) + 1;
    });
    
    console.log('📅 Sample 2025 event distribution:');
    Object.entries(dateCounts).slice(0, 10).forEach(([date, count]) => {
      console.log(`   ${date}: ${count} events`);
    });
    
    // Test 4: Check if events have proper structure
    console.log('🔍 Checking event structure...');
    if (events2025.length > 0) {
      const sampleEvent = events2025[0];
      console.log('✅ Sample event structure:');
      console.log(`   Title: ${sampleEvent.title}`);
      console.log(`   Start Date: ${sampleEvent.start_date}`);
      console.log(`   Location: ${sampleEvent.location_name}`);
      console.log(`   Type: ${sampleEvent.event_type}`);
    }
    
    return {
      totalEvents: response.data.length,
      events2025: events2025.length,
      sampleDistribution: dateCounts
    };
    
  } catch (error) {
    console.error('❌ Error testing heatmap data:', error.message);
    return null;
  }
}

// Run the test
testHeatmapData().then(result => {
  if (result) {
    console.log('\n📋 Test Results:');
    console.log(`   Total events: ${result.totalEvents}`);
    console.log(`   2025 events: ${result.events2025}`);
    console.log(`   Success rate: ${((result.events2025 / result.totalEvents) * 100).toFixed(1)}%`);
  }
}); 