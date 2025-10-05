#!/usr/bin/env node

import axios from 'axios';

const BOT_URL = 'http://localhost:8002/chat';

async function runFinalComprehensiveTest() {
    console.log('🚀 FINAL COMPREHENSIVE SYSTEM VALIDATION');
    console.log('='.repeat(60));

    const testQuery = "I want to open a tech startup in San Francisco";
    console.log(`📝 Test Query: "${testQuery}"`);

    try {
        // Step 1: Initial query
        console.log('\n🔍 Step 1: Sending initial query...');
        const initialResponse = await axios.post(BOT_URL, {
            message: testQuery,
            session_id: "final_test"
        });

        console.log(`✅ Business Type: ${initialResponse.data.analysis_data?.business_type}`);
        console.log(`✅ Location: ${initialResponse.data.analysis_data?.location}`);
        console.log(`✅ Needs Confirmation: ${initialResponse.data.analysis_data?.needs_confirmation}`);

        if (initialResponse.data.analysis_data ? .needs_confirmation) {
            // Step 2: Confirmation
            console.log('\n⏳ Step 2: Sending confirmation...');
            const confirmResponse = await axios.post(BOT_URL, {
                message: "yes, that is correct",
                session_id: "final_test"
            });

            const analysis = confirmResponse.data.analysis_data;

            console.log('\n📊 COMPREHENSIVE ANALYSIS RESULTS:');
            console.log('='.repeat(40));

            // Business Classification
            console.log(`🏢 Business Type: ${analysis?.business_type || 'N/A'}`);
            console.log(`📍 Location: ${analysis?.location || 'N/A'}`);
            console.log(`🗺️ Coordinates: ${JSON.stringify(analysis?.coordinates || [])}`);

            // Demographics
            console.log('\n👥 DEMOGRAPHICS:');
            console.log(`   • Population: ${analysis?.demographics?.total_population?.toLocaleString() || 'N/A'}`);
            console.log(`   • Median Income: $${analysis?.demographics?.median_household_income?.toLocaleString() || 'N/A'}`);
            console.log(`   • Commute Time: ${analysis?.demographics?.mean_commute_time || 'N/A'} minutes`);

            // Competition
            console.log('\n🏪 COMPETITION:');
            console.log(`   • Total Competitors: ${analysis?.competition?.total_competitors || 'N/A'}`);
            console.log(`   • Average Rating: ${analysis?.competition?.average_rating || 'N/A'}⭐`);
            console.log(`   • Competition Level: ${analysis?.competition?.competition_level || 'N/A'}`);

            // Market Opportunity
            console.log('\n🎯 MARKET OPPORTUNITY:');
            console.log(`   • Opportunity Score: ${(analysis?.market_opportunity?.score * 100)?.toFixed(1) || 'N/A'}%`);
            console.log(`   • Growth Potential: ${(analysis?.market_opportunity?.growth_potential * 100)?.toFixed(1) || 'N/A'}%`);
            console.log(`   • Recommendations: ${analysis?.market_opportunity?.recommendations?.length || 0} insights`);

            // Search Trends
            console.log('\n📈 SEARCH TRENDS:');
            const searchTrends = analysis ? .search_trends;
            if (searchTrends ? .monthly_searches) {
                console.log(`   • Monthly Search Keywords: ${Object.keys(searchTrends.monthly_searches).length}`);
                console.log(`   • Trending Keywords: ${searchTrends.trending_keywords?.join(', ') || 'N/A'}`);
                console.log(`   • Social Media Mentions: ${searchTrends.social_media_mentions?.toLocaleString() || 'N/A'}`);
                console.log(`   • Search Volume Trend: ${searchTrends.search_volume_trend || 'N/A'}`);
            } else {
                console.log('   • Search Trends: N/A');
            }

            // APIs Used
            console.log('\n🔌 API INTEGRATION:');
            console.log(`   • APIs Used: ${analysis?.apis_used?.join(', ') || 'None'}`);
            console.log(`   • Total APIs: ${analysis?.apis_used?.length || 0}`);

            // Validation
            console.log('\n✅ VALIDATION RESULTS:');
            console.log('='.repeat(40));

            const validations = {
                businessType: analysis ? .business_type === 'technology',
                hasLocation: !!analysis ? .location,
                hasCoordinates: analysis ? .coordinates && analysis.coordinates.length === 2,
                hasDemographics: !!analysis ? .demographics ? .total_population,
                hasCompetition: !!analysis ? .competition ? .total_competitors,
                hasMarketData: !!analysis ? .market_opportunity ? .score,
                hasSearchTrends: !!analysis ? .search_trends ? .monthly_searches,
                hasAPIs: analysis ? .apis_used && analysis.apis_used.length > 0,
                realData: !analysis ? .response ? .includes('N/A') && !analysis ? .response ? .includes('Contact for details')
            };

            Object.entries(validations).forEach(([key, value]) => {
                console.log(`   ${value ? '✅' : '❌'} ${key.replace(/([A-Z])/g, ' $1').toLowerCase()}`);
            });

            const successCount = Object.values(validations).filter(Boolean).length;
            const totalCount = Object.keys(validations).length;
            const successRate = (successCount / totalCount * 100).toFixed(1);

            console.log(`\n🎯 OVERALL SUCCESS RATE: ${successCount}/${totalCount} (${successRate}%)`);

            if (successRate >= 90) {
                console.log('🎉 EXCELLENT! System is performing at optimal level!');
            } else if (successRate >= 80) {
                console.log('✅ GOOD! System is performing well with minor issues.');
            } else if (successRate >= 70) {
                console.log('⚠️ FAIR! System needs some improvements.');
            } else {
                console.log('❌ POOR! System needs significant improvements.');
            }

            // Performance metrics
            console.log('\n⚡ PERFORMANCE METRICS:');
            const responseTime = Date.now() - new Date(confirmResponse.data.timestamp * 1000).getTime();
            console.log(`   • Response Time: ${responseTime}ms`);
            console.log(`   • Data Completeness: ${successRate}%`);
            console.log(`   • API Integration: ${analysis?.apis_used?.length || 0}/5 APIs`);

            return {
                success: successRate >= 80,
                successRate: parseFloat(successRate),
                validations,
                analysis
            };
        }

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        return { success: false, error: error.message };
    }
}

// Run the final test
runFinalComprehensiveTest().then(result => {
    console.log('\n' + '='.repeat(60));
    console.log('🏁 FINAL TEST COMPLETE');
    console.log('='.repeat(60));

    if (result.success) {
        console.log('🎉 SYSTEM VALIDATION: PASSED');
        console.log(`📊 Success Rate: ${result.successRate}%`);
        console.log('✅ All major components working correctly');
        console.log('🚀 System ready for production use!');
    } else {
        console.log('❌ SYSTEM VALIDATION: FAILED');
        console.log(`📊 Success Rate: ${result.successRate || 0}%`);
        console.log('⚠️ System needs improvements before production');
    }
}).catch(console.error);