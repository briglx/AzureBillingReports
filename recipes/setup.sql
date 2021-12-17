DROP DATABASE IF EXISTS [AcoRecipes]
GO
CREATE DATABASE [AcoRecipes];
GO
USE AcoRecipes;
GO

DROP SCHEMA IF EXISTS aco
GO
CREATE SCHEMA aco
GO

-- DROP TABLE IF EXISTS [aco].[Regions]
-- GO
CREATE TABLE [aco].[Regions] (
    [displayName] nvarchar(25)
    , [geographyGroup] nvarchar(20) NULL
    , [id] nvarchar(100)
    , [latitude] Decimal(8,6) NULL
    , [longitude] Decimal(9,6) NULL
    , [name] nvarchar(25)
    , [pairedRegion] nvarchar(25) NULL
    , [physicalLocation] nvarchar(35) NULL
    , [regionCategory] nvarchar(15) 
    , [regionalDisplayName] nvarchar(50)
    , [regionType] nvarchar(10)
    , [subscriptionId] nvarchar(50)
);
GO

CREATE TABLE [aco].[Advisor] (
    [assessmentKey] nvarchar(36) NULL
    , [Category] nvarchar(20)
    , [id] nvarchar(300)
    , [Impact] nvarchar(6)
    , [Impacted Resource Name] nvarchar(50)
    , [Impacted Resource Type] nvarchar(50)
    , [Last Updated] Date
    , [name] nvarchar(50)
    , [recommendationTypeId] nvarchar(50)
    , [resourceId] nvarchar(2000)
    , [score] Decimal(3,2) NULL
    , [Short Description - Problem] nvarchar(200)
    , [Short Description - Solution] nvarchar(200)
    , [source] nvarchar(300) NULL
    , [subscriptionId] nvarchar(300)
    , [type] nvarchar(50)
);
GO

CREATE TABLE [aco].[ISFData] (
    [ArmSkuName] [nvarchar](50) NULL
    , [InstanceSizeFlexibilityGroup] [nvarchar](50) NULL
	, [Ratio] Decimal(11,9)
);
GO


CREATE TABLE [aco].[Reservation Transactions] (
    [accountName] nvarchar(100)
    , [accountOwnerEmail] nvarchar(100)
    , [amount] Decimal(11,9)
    , [armSkuName] nvarchar(50)
    , [billingFrequency] nvarchar(50)
    , [costCenter] nvarchar(100)
    , [currency] nvarchar(20)
    , [currentEnrollment] nvarchar(50)
    , [departmentName] nvarchar(50)
    , [description] nvarchar(50)
    , [eventDate] Date
    , [eventType] nvarchar(10)
    , [id] nvarchar(200)
    , [name] nvarchar(50)
    , [purchasingEnrollment] nvarchar(50)
    , [purchasingSubscriptionGuid] nvarchar(50)
    , [purchasingSubscriptionName] nvarchar(50)
    , [quantity] int
    , [region] nvarchar(25)
    , [reservationOrderId] nvarchar(50)
    , [reservationOrderName] nvarchar(50)
    , [tags] nvarchar(200)
    , [term] nvarchar(5)
    , [type] nvarchar(50)
);
GO

CREATE TABLE [aco].[ActualCost](
	[InvoiceSectionName] [nvarchar](300) NULL,
	[AccountName] [nvarchar](300) NULL,
	[AccountOwnerId] [nvarchar](300) NULL,
	[SubscriptionId] [nvarchar](300) NULL,
	[SubscriptionName] [nvarchar](300) NULL,
	[ResourceGroup] [nvarchar](300) NULL,
	[ResourceLocation] [nvarchar](300) NULL,
	[Date] Date NULL,
	[ProductName] [nvarchar](300) NULL,
	[MeterCategory] [nvarchar](300) NULL,
	[MeterSubCategory] [nvarchar](300) NULL,
	[MeterId] [nvarchar](300) NULL,
	[MeterName] [nvarchar](300) NULL,
	[MeterRegion] [nvarchar](300) NULL,
	[UnitOfMeasure] [nvarchar](300) NULL,
	[Quantity] decimal (28,20) NULL,
	[EffectivePrice] decimal (28,20) NULL,
	[CostInBillingCurrency] decimal (28,20) NULL,
	[CostCenter] [nvarchar](300) NULL,
	[ConsumedService] [nvarchar](300) NULL,
	[ResourceId] [nvarchar](2000) NULL,
	[Tags] [nvarchar](4000) NULL,
	[OfferId] [nvarchar](300) NULL,
	[AdditionalInfo] [nvarchar](4000) NULL,
	[ServiceInfo1] [nvarchar](300) NULL,
	[ServiceInfo2] [nvarchar](300) NULL,
	[ResourceName] [nvarchar](300) NULL,
	[ReservationId] [nvarchar](300) NULL,
	[ReservationName] [nvarchar](300) NULL,
	[UnitPrice] decimal (28,20) NULL,
	[ProductOrderId] [nvarchar](300) NULL,
	[ProductOrderName] [nvarchar](300) NULL,
	[Term] [nvarchar](300) NULL,
	[PublisherType] [nvarchar](300) NULL,
	[PublisherName] [nvarchar](300) NULL,
	[ChargeType] [nvarchar](300) NULL,
	[Frequency] [nvarchar](300) NULL,
	[PricingModel] [nvarchar](300) NULL,
	[AvailabilityZone] [nvarchar](300) NULL,
	[BillingAccountId] [nvarchar](300) NULL,
	[BillingAccountName] [nvarchar](300) NULL,
	[BillingCurrencyCode] [nvarchar](20) NULL,
	[BillingPeriodStartDate] date NULL,
	[BillingPeriodEndDate] date NULL,
	[BillingProfileId] [nvarchar](100) NULL,
	[BillingProfileName] [nvarchar](300) NULL,
	[InvoiceSectionId] [nvarchar](300) NULL,
	[IsAzureCreditEligible] [nvarchar](10) NULL,
	[PartNumber] [nvarchar](50) NULL,
	[PayGPrice] [nvarchar](100) NULL,
	[PlanName] [nvarchar](300) NULL,
	[ServiceFamily] [nvarchar](300) NULL,
	[CostAllocationRuleName] [nvarchar](300) NULL
);
GO

CREATE TABLE [aco].[AmortizedCost] (
    [InvoiceSectionName] [nvarchar](300) NULL,
    [AccountName] [nvarchar](300) NULL,
    [AccountOwnerId] [nvarchar](300) NULL,
    [SubscriptionId] [nvarchar](300) NULL,
    [SubscriptionName] [nvarchar](300) NULL,
    [ResourceGroup] [nvarchar](300) NULL,
    [ResourceLocation] [nvarchar](300) NULL,
    [Date] date NULL,
    [ProductName] [nvarchar](300) NULL,
    [MeterCategory] [nvarchar](300) NULL,
    [MeterSubCategory] [nvarchar](300) NULL,
    [MeterId] [nvarchar](300) NULL,
    [MeterName] [nvarchar](300) NULL,
    [MeterRegion] [nvarchar](300) NULL,
    [UnitOfMeasure] [nvarchar](300) NULL,
    [Quantity] decimal (28,20) NULL,
    [EffectivePrice] decimal (28,20) NULL,
    [CostInBillingCurrency] decimal (28,20) NULL,
    [CostCenter] [nvarchar](300) NULL,
    [ConsumedService] [nvarchar](300) NULL,
    [ResourceId] [nvarchar](2000) NULL,
    [Tags] [nvarchar](4000) NULL,
    [OfferId] [nvarchar](300) NULL,
    [AdditionalInfo] [nvarchar](4000) NULL,
    [ServiceInfo1] [nvarchar](300) NULL,
    [ServiceInfo2] [nvarchar](300) NULL,
    [ResourceName] [nvarchar](300) NULL,
    [ReservationId] [nvarchar](300) NULL,
    [ReservationName] [nvarchar](300) NULL,
    [UnitPrice] decimal (28,20) NULL,
    [ProductOrderId] [nvarchar](300) NULL,
    [ProductOrderName] [nvarchar](300) NULL,
    [Term] [nvarchar](300) NULL,
    [PublisherType] [nvarchar](300) NULL,
    [PublisherName] [nvarchar](300) NULL,
    [ChargeType] [nvarchar](300) NULL,
    [Frequency] [nvarchar](300) NULL,
    [PricingModel] [nvarchar](300) NULL,
    [AvailabilityZone] [nvarchar](300) NULL,
    [BillingAccountId] [nvarchar](300) NULL,
    [BillingAccountName] [nvarchar](300) NULL,
    [BillingCurrencyCode] [nvarchar](20) NULL,
    [BillingPeriodStartDate] date NULL,
    [BillingPeriodEndDate] date NULL,
    [BillingProfileId] [nvarchar](100) NULL,
    [BillingProfileName] [nvarchar](300) NULL,
    [InvoiceSectionId] [nvarchar](300) NULL,
    [IsAzureCreditEligible] [nvarchar](10) NULL,
    [PartNumber] [nvarchar](50) NULL,
    [PayGPrice] [nvarchar](100) NULL,
    [PlanName] [nvarchar](300) NULL,
    [ServiceFamily] [nvarchar](300) NULL,
    [CostAllocationRuleName] [nvarchar](300) NULL
);
GO

CREATE TABLE [aco].[Reservation Details] (
    [InstanceFlexibilityGroup] [nvarchar](300) NULL,
    [InstanceFlexibilityRatio] [nvarchar](300) NULL,
    [InstanceId] [nvarchar](2000) NULL,
    [Kind] [nvarchar](300) NULL,
    [ReservationId] [nvarchar](300) NULL,
    [ReservationOrderId] [nvarchar](300) NULL, 
    [ReservedHours] decimal (28,10) NULL,
    [SkuName] [nvarchar](300) NULL,
    [TotalReservedQuantity] decimal (28,10) NULL,
    [UsageDate] [nvarchar](30) NULL,
    [UsedHours] decimal (28,10) NULL
);
GO

-- Build from Billing data
-- CREATE TABLE Subscriptions (
--     SubscriptionId nvarchar(max)
--     , SubscriptionName nvarchar(max)
-- );
-- GO

CREATE TABLE [aco].[Reservation Recommendations] (
    [costWithNoReservedInstances] decimal (28,10)
    , [firstUsageDate] nvarchar(max)
    , [id nvarchar(max)
    , [instanceFlexibilityGroup] nvarchar(max)
    , [instanceFlexibilityRatio] nvarchar(max)
    , [kind] nvarchar(max)
    , [location] nvarchar(max)
    , [Look Back Period] nvarchar(max)
    , [meterId] nvarchar(max)
    , [name] nvarchar(max)
    , [netSavings] decimal (28,10)
    , [normalizedSize] nvarchar(max)
    , [Recommended Quantity] decimal (28,10)
    , [recommendedQuantityNormalized] nvarchar(max)
    , [Reservation Scope] nvarchar(max)
    , [Reservation Term] nvarchar(max)
    , [sku] nvarchar(max)
    , [skuProperties] nvarchar(max)
    , [subscriptionId] nvarchar(max)
    , [totalCostWithReservedInstances] decimal (28,10)
    , [type] nvarchar(max)
);
GO

-- Build from Reservation Recommendations
-- CREATE TABLE Meters (
--     meterId nvarchar(max)
-- );
-- GO

CREATE TABLE [aco].[PriceList] (
    [billingPeriodId] nvarchar(max)
    , [meterCategory] nvarchar(max)
    , [meterId] nvarchar(max)
    , [meterLocation] nvarchar(max)
    , [meterName] nvarchar(max)
    , [meterSubCategory] nvarchar(max)
    , [unit] nvarchar(max)
);
GO

CREATE TABLE [aco].[MarketPlace] (
    [accountName] nvarchar(max)
    , [additionalInfo] nvarchar(max)
    , [billingPeriodId] nvarchar(max)
    , [consumedQuantity] nvarchar(max)
    , [costCenter] nvarchar(max)
    , [currency] nvarchar(max)
    , [departmentName] nvarchar(max)
    , [id] nvarchar(max)
    , [instanceId] nvarchar(max)
    , [instanceName] nvarchar(max)
    , [isEstimated] nvarchar(max)
    , [isRecurringCharge] nvarchar(max)
    , [meterId] nvarchar(max)
    , [name] nvarchar(max)
    , [offerName] nvarchar(max)
    , [orderNumber] nvarchar(max)
    , [planName] nvarchar(max)
    , [pretaxCost] nvarchar(max)
    , [publisherName] nvarchar(max)
    , [resourceGroup] nvarchar(max)
    , [resourceRate] nvarchar(max)
    , [subscriptionGuid] nvarchar(max)
    , [subscriptionName] nvarchar(max)
    , [tags] nvarchar(max)
    , [type] nvarchar(max)
    , [unitOfMeasure] nvarchar(max)
    , [usageEnd] nvarchar(max)
    , [usageStart] nvarchar(max)
);
GO