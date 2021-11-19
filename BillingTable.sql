-- Create Temple Table
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
drop TABLE [dbo].[BillingAmortized];
CREATE TABLE [dbo].[BillingAmortized]
(
    
    [InvoiceSectionName] nvarchar(max) NULL,
    [AccountName] nvarchar(max) NULL,
    [AccountOwnerId] nvarchar(max) NULL,
    [SubscriptionId] nvarchar(max) NULL,
    [SubscriptionName] nvarchar(max) NULL,
    [ResourceGroup] nvarchar(max) NULL,
    [ResourceLocation] nvarchar(max) NULL,
    [Date] nvarchar(25) NULL,
    [ProductName] nvarchar(max) NULL,
    [MeterCategory] nvarchar(max) NULL,
    [MeterSubCategory] nvarchar(max) NULL,
    [MeterId] nvarchar(100) NULL,
    [MeterName] nvarchar(max) NULL,
    [MeterRegion] nvarchar(max) NULL,
    [UnitOfMeasure] nvarchar(max) NULL,
    [Quantity] nvarchar(max) NULL,
    [EffectivePrice] nvarchar(max) NULL,
    [CostInBillingCurrency] nvarchar(max) NULL,
    [CostCenter] nvarchar(max) NULL,
    [ConsumedService] nvarchar(max) NULL,
    [ResourceId] varchar(100) NULL,
    [Tags] nvarchar(max) NULL,
    [OfferId] nvarchar(max) NULL,
    [AdditionalInfo] nvarchar(max) NULL,
    [ServiceInfo1] nvarchar(max) NULL,
    [ServiceInfo2] nvarchar(max) NULL,
    [ResourceName] nvarchar(max) NULL,
    [ReservationId] nvarchar(max) NULL,
    [ReservationName]nvarchar(max) NULL,
    [UnitPrice] nvarchar(max) NULL,
    [ProductOrderId] nvarchar(max) NULL,
    [ProductOrderName] nvarchar(max) NULL,
    [Term] nvarchar(max) NULL,
    [PublisherType] nvarchar(max) NULL,
    [PublisherName] nvarchar(max) NULL,
    [ChargeType] nvarchar(max) NULL,
    [Frequency] nvarchar(max) NULL,
    [PricingModel] nvarchar(max) NULL,
    [AvailabilityZone] nvarchar(max) NULL,
    [BillingAccountId] nvarchar(max) NULL,
    [BillingAccountName] nvarchar(max) NULL,
    [BillingCurrencyCode] nvarchar(max) NULL,
    [BillingPeriodStartDate] nvarchar(max) NULL,
    [BillingPeriodEndDate] nvarchar(max) NULL,
    [BillingProfileId] nvarchar(max) NULL,
    [BillingProfileName] nvarchar(max) NULL,
    [InvoiceSectionId] nvarchar(max) NULL,
    [IsAzureCreditEligible] nvarchar(max) NULL,
    [PartNumber] nvarchar(max) NULL,
    [PayGPrice] nvarchar(max) NULL,
    [PlanName] nvarchar(max) NULL,
    [ServiceFamily] nvarchar(max) NULL,
    [CostAllocationRuleName] nvarchar(max) NULL

)

GO