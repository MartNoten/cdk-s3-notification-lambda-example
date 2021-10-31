import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as lambda from '@aws-cdk/aws-lambda';
import * as lambdaEventSources from '@aws-cdk/aws-lambda-event-sources';

export class CdkBankStatementsAnalysisStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'MyBankStatements', {
      autoDeleteObjects: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    
    const lambdaFunction = new lambda.Function(this, 'BankAnalyser', {
      code: lambda.Code.fromAsset('lambda/BankStatementAnalyzer'),
      handler: 'StatementAnalyzer.handler',
      functionName: 'StatementAnalyzer',
      runtime: lambda.Runtime.PYTHON_3_9,
    });

    const s3PutEventSource = new lambdaEventSources.S3EventSource(bucket, {
      events: [
        s3.EventType.OBJECT_CREATED_PUT
      ]
    });

    lambdaFunction.addEventSource(s3PutEventSource);
    bucket.grantReadWrite(lambdaFunction);
  }
}
