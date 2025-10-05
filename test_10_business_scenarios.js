#!/usr/bin/env node

import axios from 'axios';

const BOT_URL = 'http://localhost:8002/chat';

// Test scenarios: 10 different business types across USA
const testScenarios = [{
        id: 1,
        business: "burger shop",
        location: "Miami, FL",
        expectedType: "restaurant",
        description: "Fast food restaurant in Miami"
    },
    {
        id: 2,
        business: "gym",
        location: "Seattle, WA",
        expectedType: "health_wellness",
        description: "Fitness center in Seattle"
    },
    {
        id: 3,
        business: "auto repair shop",
        location: "Denver, CO",
        expectedType: "automotive",
        description: "Car repair service in Denver"
    },
    {
        id: 4,
        business: "tech startup",
        location: "San Francisco, CA",
        expectedType: "technology",
        description: "Technology company in San Francisco"
    },
    {
        id: 5,
        business: "clothing store",
        location: "New York, NY",
        expectedType: "retail",
        description: "Fashion retail in New York"
    },
    {
        id: 6,
        business: "accounting firm",
        location: "Chicago, IL",
        expectedType: "professional_services",
        description: "Professional services in Chicago"
    },
    {
        id: 7,
        business: "pizza restaurant",
        location: "Austin, TX",
        expectedType: "restaurant",
        description: "Italian restaurant in Austin"
    },
    {
        id: 8,
        business: "beauty salon",
        location: "Las Vegas, NV",
        expectedType: "health_wellness",
        description: "Beauty services in Las Vegas"
    },
    {
        id: 9,
        business: "electronics store",
        location: "Phoenix, AZ",
        expectedType: "retail",
        description: "Electronics retail in Phoenix"
    },
    {
        id: 10,
        business: "mini car shop",
        location: "Portland, OR",
        expectedType: "automotive",
        description: "Automotive services in Portland"
    }
];

async function testBusinessScenario(scenario) {
    console.log(`\n🧪 Testing Scenario ${scenario.id}: ${scenario.description}`);
    console.log(`📝 Query: "I want to open a ${scenario.business} in ${scenario.location}"`);

    try {
        // Step 1: Send initial query
        const initialResponse = await axios.post(BOT_URL, {
            message: `I want to open a ${scenario.business} in ${scenario.location}`,
            session_id: `test_${scenario.id}`
        });

        console.log(`✅ Initial Response: ${initialResponse.data.response.substring(0, 100)}...`);
        console.log(`🔍 Detected Business Type: ${initialResponse.data.analysis_data?.business_type || 'Not detected'}`);
        console.log(`📍 Detected Location: ${initialResponse.data.analysis_data?.location || 'Not detected'}`);

        // Check if confirmation is needed
        if (initialResponse.data.analysis_data ? .needs_confirmation) {
            console.log(`⏳ Confirmation needed, sending confirmation...`);

            // Step 2: Send confirmation
            const confirmResponse = await axios.post(BOT_URL, {
                message: "yes, that is correct",
                session_id: `test_${scenario.id}`
            });

            console.log(`✅ Confirmation Response: ${confirmResponse.data.response.substring(0, 100)}...`);

            // Analyze the final response
            const analysisData = confirmResponse.data.analysis_data;

            console.log(`📊 Analysis Results:`);
            console.log(`   • Business Type: ${analysisData?.business_type || 'N/A'}`);
            console.log(`   • Location: ${analysisData?.location || 'N/A'}`);
            console.log(`   • Coordinates: ${JSON.stringify(analysisData?.coordinates || [])}`);
            console.log(`   • Competition: ${analysisData?.competition?.total_competitors || 0} competitors`);
            console.log(`   • Demographics: ${analysisData?.demographics?.total_population || 0} people`);
            console.log(`   • Search Trends: ${Object.keys(analysisData?.search_trends?.monthly_searches || {}).length} keywords`);
            console.log(`   • APIs Used: ${analysisData?.apis_used?.join(', ') || 'None'}`);

            // Validate results
            const isCorrectType = analysisData ? .business_type === scenario.expectedType;
            const hasCoordinates = analysisData ? .coordinates && analysisData.coordinates.length === 2;
            const hasRealData = analysisData ? .apis_used && analysisData.apis_used.length > 0;

            console.log(`🎯 Validation:`);
            console.log(`   • Correct Business Type: ${isCorrectType ? '✅' : '❌'} (Expected: ${scenario.expectedType}, Got: ${analysisData?.business_type})`);
            console.log(`   • Has Coordinates: ${hasCoordinates ? '✅' : '❌'}`);
            console.log(`   • Has Real Data: ${hasRealData ? '✅' : '❌'}`);

            return {
                scenario: scenario.id,
                success: isCorrectType && hasCoordinates && hasRealData,
                businessType: analysisData ? .business_type,
                expectedType: scenario.expectedType,
                hasCoordinates,
                hasRealData,
                apisUsed: analysisData ? .apis_used ? .length || 0
            };
        } else {
            console.log(`⚠️ No confirmation needed, but expected confirmation flow`);
            return {
                scenario: scenario.id,
                success: false,
                businessType: initialResponse.data.analysis_data ? .business_type,
                expectedType: scenario.expectedType,
                hasCoordinates: false,
                hasRealData: false,
                apisUsed: 0
            };
        }

    } catch (error) {
        console.error(`❌ Error testing scenario ${scenario.id}:`, error.message);
        return {
            scenario: scenario.id,
            success: false,
            error: error.message
        };
    }
}

async function runAllTests() {
    console.log('🚀 Starting Comprehensive Business Scenario Testing');
    console.log('='.repeat(60));

    const results = [];

    for (const scenario of testScenarios) {
        const result = await testBusinessScenario(scenario);
        results.push(result);

        // Small delay between tests
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Summary
    console.log('\n' + '='.repeat(60));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(60));

    const successful = results.filter(r => r.success).length;
    const total = results.length;

    console.log(`✅ Successful Tests: ${successful}/${total}`);
    console.log(`❌ Failed Tests: ${total - successful}/${total}`);

    console.log('\n📋 Detailed Results:');
    results.forEach(result => {
        const status = result.success ? '✅' : '❌';
        console.log(`   ${status} Scenario ${result.scenario}: ${result.businessType || 'N/A'} (Expected: ${result.expectedType})`);
        if (result.error) {
            console.log(`      Error: ${result.error}`);
        }
    });

    // Business type accuracy
    const correctTypes = results.filter(r => r.businessType === r.expectedType).length;
    console.log(`\n🎯 Business Type Classification Accuracy: ${correctTypes}/${total} (${(correctTypes/total*100).toFixed(1)}%)`);

    // API usage
    const withAPIs = results.filter(r => r.apisUsed > 0).length;
    console.log(`🔌 API Integration Success: ${withAPIs}/${total} (${(withAPIs/total*100).toFixed(1)}%)`);

    // Coordinate accuracy
    const withCoords = results.filter(r => r.hasCoordinates).length;
    console.log(`🗺️ Coordinate Accuracy: ${withCoords}/${total} (${(withCoords/total*100).toFixed(1)}%)`);

    console.log('\n🎉 Testing Complete!');
}

// Run the tests
runAllTests().catch(console.error);